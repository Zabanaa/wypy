from termcolor import colored
from prettytable import PrettyTable
from dbus.exceptions import DBusException
from wypy.utils.constants import (
    NM_CONNECTION_IFACE,
    NM_BUS_NAME,
    NM_OBJ_PATH,
    NM_SETTINGS_IFACE,
    NM_SETTINGS_OBJ_PATH,
    DBUS_GENERAL_PROPS,
    NM_IFACE,
    NM_DEVICE_IFACE,
    NM_WIRELESS_IFACE,
    NM_ACCESS_POINT_IFACE,
)
from wypy.wypy import WyPy
import dbus, click, sys, time, uuid  # noqa E401


class WiFi(WyPy):

    def __init__(self):
        super().__init__()
        self.proxy = self.bus.get_object(NM_BUS_NAME, NM_OBJ_PATH)
        self.wifi_prop = 'WirelessEnabled'
        self.status_table = PrettyTable(['SSID', 'MODE', 'RATE', 'SIGNAL', 'BARS'])  # noqa E501
        self.status_table.align = 'l'
        self.status_table.border = False
        self.status_table.sortby = 'SIGNAL'
        self.status_table.left_padding_width = 0
        self.status_table.right_padding_width = 8
        self.settings_obj = self.bus.get_object(
            NM_BUS_NAME,
            NM_SETTINGS_OBJ_PATH
        )
        self.settings_iface = dbus.Interface(
            self.settings_obj,
            NM_SETTINGS_IFACE
        )
        self.wifi_dev_path = self._get_wireless_device_path()
        self.wifi_dev_obj = self.bus.get_object(
            NM_BUS_NAME,
            self.wifi_dev_path
        )
        self.wifi_iface = dbus.Interface(self.wifi_dev_obj, NM_WIRELESS_IFACE)

    def list_access_points(self):
        """
        Lists all visible access points.
        """
        click.echo("Scanning for available access points ...")
        access_points = self._get_all_access_points()
        rows = list(map(self._create_row, access_points))

        for row in rows:
            self.status_table.add_row(row)

        click.echo(self.status_table)

    def rescan(self):
        """
        Rescans the network for ( potentially ) newly added access points.
        """
        click.echo('Performing rescan ...')
        self._request_scan()
        click.echo('Done !')

    def connect(self):
        """
            # - get all connections
            - is there a matching known connection with that name ?
                - if so is it active ?
                    - if it's not active activate it
            - if there is no matching connection
            - add and activate one passing it the type,
            name, and password (as per the example on github)
        """
        conns_paths = self._list_all_connections()
        conns_info = list(map(self._get_connection_info, conns_paths))
        conn_names = list(map(lambda conn: str(conn['id']), conns_info))

        access_point_name = click.prompt('SSID name')
        access_point_password = click.prompt('Password')

        if access_point_name in conn_names:
            _filter = lambda conn: conn['id'] == access_point_name  # noqa E731
            conn_to_activate = next(filter(_filter, conns_info))
            conn_path = conn_to_activate['dbus_path']
            active_conn_path = self._activate_existing_connection(conn_path)
            click.echo(f'Connection to {access_point_name} successful ! (D-Bus path: {active_conn_path})')  # noqa E501
        else:
            self._connect_to_access_point(
                access_point_name,
                access_point_password
            )

    def turn_on(self):
        """
        Enables the network card's wireless capability.
        """
        click.echo('Enabling WiFi ...')
        wifi_enabled = self._get_wifi_status_code()
        if not wifi_enabled:
            self._enable_wifi()
        else:
            click.echo('WiFi is already enabled. Skipping.')

    def turn_off(self):
        """
        Disables the network card's wireless capability.
        """
        click.echo('Disabling WiFi ...')
        wifi_enabled = self._get_wifi_status_code()
        if wifi_enabled:
            self._disable_wifi()
        else:
            click.echo('WiFi is already disabled. Skipping.')

    def print_status(self):
        """
        Prints the current wifi status to the user.
        """
        status_code = self._get_wifi_status_code()
        prop = DBUS_GENERAL_PROPS[self.wifi_prop]
        status = self.translate_status_code(prop, status_code)
        click.echo(f'WiFi is {status}')

    #   ---------------
    #
    #   Private Methods
    #
    #   ---------------

    def _connect_to_access_point(self, ap_name, ap_pwd):
        """
        Establishes a wireless connection to the
        provided access point.

        Arguments:
            ap_name {string} -- the access point's name (SSID)
            ap_pwd {string} -- the access point's password
        """

        all_access_points = self._get_all_access_points()

        _filter = lambda ap: ap['ssid'] == ap_name  # noqa E731
        ap_to_connect_to = next(filter(_filter, all_access_points), None)

        if ap_to_connect_to is not None:
            ap_path = ap_to_connect_to['dbus_path']
            conn_info = self._generate_wireless_connection_info(
                ap_name,
                ap_pwd
            )
            click.echo('Establishing connection. Please hold tight ...')
            self._establish_connection(conn_info, ap_path)
        else:
            msg = f'[Error]: Connection to {ap_name} impossible. No such access point.'  # noqa E501
            sys.exit(colored(msg, "red"))

    def _handle_wifi_state_change(self, new_state, old_state, reason):
        if new_state == 100:
            msg = f'Connection to {self.ap_name} ({self.ap_uuid}) successful !'
            self._exit_loop(msg)

        if new_state == 120:
            if reason == 7:
                msg = '[Error]. Could not connect. Invalid Password.'
            else:
                msg = f'[Error] Could not connect. Reason number: {reason}'

            self._exit_loop(msg, error=True)

    def _establish_connection(self, conn, ap_path):
        from gi.repository import GObject  # noqa F401

        nm = dbus.Interface(self.proxy, NM_IFACE)
        settings, active_conn = nm.AddAndActivateConnection(
            conn,
            self.wifi_dev_path,
            ap_path
        )
        try:
            self.wifi_dev_obj.connect_to_signal(
                'StateChanged',
                self._handle_wifi_state_change,
                NM_DEVICE_IFACE,
            )
            self.ap_name = conn['connection']['id']
            self.ap_uuid = conn['connection']['uuid']
        except DBusException as exc:
            msg = exc.get_dbus_message()
            sys.exit(msg)

        self.loop = GObject.MainLoop()
        self.loop.run()

    def _generate_wireless_connection_info(self, ap_name, ap_pwd):
        conn = dbus.Dictionary({
            'type': '802-11-wireless',
            'uuid': str(uuid.uuid4()),
            'id': ap_name
        })

        settings_wifi = dbus.Dictionary({
            'ssid': dbus.ByteArray(ap_name.encode('utf-8')),
            'mode': 'infrastructure'
        })

        settings_wifi_security = dbus.Dictionary({
            'key-mgmt': 'wpa-psk',
            'auth-alg': 'open',
            'psk': ap_pwd
        })

        settings_ipv4 = dbus.Dictionary({'method': 'auto'})
        settings_ipv6 = dbus.Dictionary({'method': 'ignore'})

        return dbus.Dictionary({
            'connection': conn,
            '802-11-wireless': settings_wifi,
            '802-11-wireless-security': settings_wifi_security,
            'ipv4': settings_ipv4,
            'ipv6': settings_ipv6
        })

    def _activate_existing_connection(self, conn_path):
        """
        Activates an existing connection by calling the
        ActivateConnection method available on the main NetworkManager
        interface.
        If the connection attempt fails, the program exits with
        the error message returned by D-Bus.

        Arguments:
            conn_path {string} -- the connection's own d-bus path

        Returns:
            string -- the newly activated connection's object path
        """
        self.nm = dbus.Interface(self.proxy, NM_IFACE)
        try:
            active_conn = self.nm.ActivateConnection(
                conn_path,
                self.wifi_dev_path,
                '/'
            )
        except DBusException as exc:
            msg = exc.get_dbus_message()
            sys.exit(msg)
        else:
            return active_conn

    def _get_connection_info(self, conn_path):
        conn_obj = self.bus.get_object(NM_BUS_NAME, conn_path)
        conn_iface = dbus.Interface(conn_obj,  NM_CONNECTION_IFACE)
        conn_info = conn_iface.GetSettings()['connection']
        conn_info['dbus_path'] = conn_path
        return conn_info

    def _list_all_connections(self):
        return self.settings_iface.ListConnections()

    def _enable_wifi(self):
        """
        Sets the 'WirelessEnabled' property to False
        on the main NetworkManager d-bus interface.
        """
        self.set_object_property(
            proxy=self.proxy,
            prop_name=self.wifi_prop,
            value=True
        )

    def _disable_wifi(self):
        """
        Sets the 'WirelessEnabled' property to False
        on the main NetworkManager d-bus interface.
        """
        self.set_object_property(
            proxy=self.proxy,
            prop_name=self.wifi_prop,
            value=False
        )

    def _get_wifi_status_code(self):
        """
        Retrieves the current status code for
        wireless connectivity.

        Returns:
            string -- wifi status code
        """
        return self.get_object_property(
            proxy=self.proxy,
            prop_name=self.wifi_prop
        )

    def _create_row(self, ap_data):
        """
        Creates a PrettyTable row using the access point's
        values.
        This function will color the row according to the
        value of the 'signal' key.

        Arguments:
            ap_data {dict} -- the access point's infomation

        Returns:
            list -- [description]
        """
        del ap_data['dbus_path']

        signal = ap_data['signal']
        values = ap_data.values()

        if signal in range(0, 31):
            color = "cyan"
        elif signal in range(30, 61):
            color = "magenta"
        elif signal in range(60, 81):
            color = "yellow"
        elif signal in range(80, 101):
            color = "green"
        else:
            color = "white"

        return list(map(lambda val: colored(val, color), values))

    def _get_wireless_device_path(self):
        """
        Gets the d-bus object path for the wireless device(s)
        _Note_: in this current implementation, we return the object path
        for the first wireless device returned. Support for multiple devices
        will be added in the coming versions.

        Returns:
            string -- the d-bus object path for the wireless device
        """
        devices_paths = self._get_all_devices_paths()
        all_devices = list(map(lambda dev: self.get_all_properties(dev, NM_DEVICE_IFACE), devices_paths))  # noqa E501
        wireless_devices = list(filter(self._is_device_wifi, zip(devices_paths, all_devices)))  # noqa E501

        try:
            wifi_dev_path = wireless_devices[0]  # extract the first real wifi device that's returned  # noqa E501
        except Exception:
            err_msg = '[Error]: No wireless device found'
            sys.exit(colored(err_msg, "red"))
        else:
            return wifi_dev_path[0]

    def _get_all_devices_paths(self):
        """
        Gets object path for all available devices.

        Returns:
            list -- list of object paths for all devices
        """
        nm = dbus.Interface(self.proxy, NM_IFACE)
        return nm.GetAllDevices()

    def _is_device_wifi(self, device):
        """
        Checks if the provided device is both real and wireless enabled.
        This is done by checking the 'Real' and 'DeviceType' properties on
        the given device.

        Arguments:
            device {device} -- the device tuple containing the dbus object
            path at index [0] and the actual dictionary of info at index [1]

        Returns:
            bool -- whether the device is wireless
        """
        device_info = device[1]
        real, device_type = device_info['Real'], device_info['DeviceType']
        return bool(real) and device_type == 2

    def _get_all_access_points(self):
        """
        Gets information for all visible access points
        on the network.

        Arguments:
            wifi_iface {dbus.Interface} -- the wireless interface
            to call GetAllAccessPoints on

        Returns:
            list -- access points dictionaries
        """

        try:
            self._request_scan()
        except SystemExit:
            time.sleep(4)

        access_points_paths = self._list_ap_paths()
        access_points = list(map(self._extract_ap_info, access_points_paths))
        return access_points

    def _list_ap_paths(self):
        """
        Calls GetAllAccessPoints on the wireless d-bus
        interface provided by NetworkManager.

        Arguments:
            wifi_iface {dbus.Interface} -- the wireless interface
            to call GetAllAccessPoints on

        Returns:
            list -- list of access points object paths
        """
        return self.wifi_iface.GetAllAccessPoints()

    def _request_scan(self):
        """
        Calls RequestScan on the wireless d-bus interface
        provided by NetworkManager.

        Arguments:
            wifi_iface {dbus.Interface} -- the wireless interface
            to call RequestScan on
        """
        try:
            self.wifi_iface.RequestScan({})
        except DBusException as exc:
            msg = exc.get_dbus_message()
            err = "Scanning not allowed immediately following previous scan"
            if msg == err:
                sys.exit(colored(f"[Error]: {msg}", "red"))

    def _extract_ap_info(self, ap_path):
        """
        Extract necessary access point properties.
        Namely:
            - the ssid
            - the mode
            - the bitrate
            - the signal strength
            - the bars (visual representation of signal strength)
            - the dbus object path

        Arguments:
            ap_path {string} -- the access point's own d-bus object path

        Returns:
            dict -- access point info
        """
        props = self.get_all_properties(ap_path, NM_ACCESS_POINT_IFACE)
        return {
            'ssid': self._get_ssid(props.get('Ssid')),
            'mode': self._get_mode(props.get('Mode', '--')),
            'rate': self._format_bitrate(props.get('MaxBitrate')),
            'signal': int(props.get('Strength', '--')),
            'bars': self._get_bars(props.get('Strength')),
            'dbus_path': ap_path

        }

    def _get_ssid(self, ssid_byte_list):
        """
        Translates ssid from byte list to string.
        Arguments:
            ssid_byte_list {list} -- the raw ssid in byte form

        Returns:
            string -- the ssid name
        """
        if len(ssid_byte_list) == 0:
            return "--"

        ssid = ""
        for char in ssid_byte_list:
            ssid = ssid + chr(char)

        return ssid

    def _get_bars(self, signal):
        """
        Visually describes signal strength by assigning
        it to a number or bars (*)

        Arguments:
            signal {string} -- the device's signal strength

        Returns:
            string -- the number or bars
        """
        signal = int(signal)
        if signal in range(0, 30):
            return "*"
        elif signal in range(30, 60):
            return "**"
        elif signal in range(60, 80):
            return "***"
        elif signal in range(80, 101):
            return "****"
        else:
            return "--"

    def _get_mode(self, mode):
        """
        Convert device mode integer to its string equivalent.

        Arguments:
            mode {str} -- the device mode

        Returns:
            string -- the corresponding human readable mode
        """
        mode = int(mode)
        if mode == 4:
            return "Mesh"

        if mode == 3:
            return "Access Point"

        if mode == 2:
            return "Infra"

        if mode == 1:
            return "Ad Hoc"

        if mode == 0:
            return "Unknown"

    def _format_bitrate(self, bitrate):
        """
        Convert bitrate value into a human readable string

        Arguments:
            bitrate {float} -- bitrate

        Returns:
            string -- human readable bitrate
        """
        bitrate = int(bitrate) // 1000
        return f"{bitrate} Mbit/s"

    def _exit_loop(self, msg, error=False):
        """
        Exit the main D-bus loop

        Arguments:
            msg {string} -- the message to display the user

        Keyword Arguments:
            error {bool} -- if the message is an error (default: {False})
        """
        if error:
            msg = colored(msg, 'red')
        click.echo(msg)
        self.loop.quit()
