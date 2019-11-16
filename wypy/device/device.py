from wypy.utils.helpers import format_list, format_table_key
from prettytable import PrettyTable
from termcolor import colored
from wypy.wypy import WyPy
from wypy.utils.constants import (
    NM_BUS_NAME,
    NM_OBJ_PATH,
    NM_IFACE,
    NM_DEVICE_IFACE,
    NM_ACTIVE_CONN_IFACE,
    IP4_CONFIG_IFACE
)
import sys
import click
import dbus
from dbus.exceptions import DBusException


class Device(WyPy):

    def __init__(self):
        super().__init__()
        self.nm = self.bus.get_object(NM_BUS_NAME, NM_OBJ_PATH)
        self.status_table_keys = ['DEVICE', 'TYPE', 'STATE', 'CONNECTION']
        self.status_table = PrettyTable(self.status_table_keys)
        self.status_table.align = 'l'
        self.all_devices = self.get_object_property(
            proxy=self.nm,
            bus_name=NM_IFACE,
            prop_name='AllDevices'
        )
        self.known_device_names = []
        self.details_table = PrettyTable(['PROPERTY', 'VALUE'])
        self.details_table.align = 'l'

    def print_status(self):
        """
        Displays general device status information to the user.
        """
        click.echo('Showing status ...')
        device_status = list(map(self._get_device_status, self.all_devices))  # noqa E501
        sorted_status = sorted(device_status, key=lambda k: (k['connection'], k['type']), reverse=True)  # noqa E501
        rows = list(map(self._create_row, sorted_status))

        for row in rows:
            self.status_table.add_row(row)

        click.echo(self.status_table)

    def list_all(self):
        """
        Prints a table with detailed information for each known device.
        """
        click.echo('Listing all devices ...')
        for device in self.all_devices:
            details = self._get_device_details(device)
            self._fill_details_table(details)

            click.echo(self.details_table)
            self.details_table.clear_rows()

    def print_details(self, ifname):
        """
        Prints a table with details information for the given device.

        Arguments:
            ifname {[string]} -- [the device to display the details for]
        """
        try:
            device_path = self._get_known_device_object_path(ifname)
        except ValueError as exc:
            sys.exit(colored(str(exc), "red"))
        else:
            device_details = self._get_device_details(device_path, show_all=True)  # noqa E501

        self._fill_details_table(device_details)

        click.echo(self.details_table)

    def update_ifname_connection(self, ifname):
        """
        Updates the given device's connection information.
        This is a clone of the "nmcli device update/reapply" command.

        Arguments:
            ifname {string} -- [the device to perform the action on]
        """
        try:
            device_path = self._get_known_device_object_path(ifname)
        except ValueError as exc:
            sys.exit(colored(exc.args, "red"))
        else:
            self._update_connection(device_path, ifname)

    def disconnect(self, ifname):
        """
        Disconnects the given device.

        Arguments:
            ifname {string} -- the device to disconnect
        """
        try:
            device_path = self._get_known_device_object_path(ifname)
        except ValueError as exc:
            sys.exit(colored(exc.args, "red"))
        else:
            self._disconnect_device(device_path, ifname)

    def delete_iface(self, ifname):
        """
        Deletes the given device

        Arguments:
            ifname {string} -- the device to delete
        """
        try:
            device_path = self._get_known_device_object_path(ifname)
        except ValueError as exc:
            sys.exit(colored(exc.args, "red"))
        else:
            self._delete_iface(device_path, ifname)

    def manage(self, ifname, flag=True):
        """
        Sets the given device's Managed property
        to either True of False.

        Arguments:
            ifname {string} -- [the device to manage / unmanage]

        Keyword Arguments:
            flag {bool} -- [manage flag] (default: {True})
        """
        try:
            device_path = self._get_known_device_object_path(ifname)
        except ValueError as exc:
            sys.exit(colored(exc.args, "red"))
        else:
            proxy = self.bus.get_object(NM_BUS_NAME, device_path)
            self.set_object_property(
                proxy,
                bus_name=NM_DEVICE_IFACE,
                prop_name='Managed',
                value=flag
            )

    def autoconnect(self, ifname, flag=True):
        """
        Sets the given device's Autoconnect property
        to either True of False.

        Arguments:
            ifname {string} -- [the device to autoconnect]

        Keyword Arguments:
            flag {bool} -- [enable / disable auto connect] (default: {True})
        """
        try:
            device_path = self._get_known_device_object_path(ifname)
        except ValueError as exc:
            sys.exit(colored(exc.args, "red"))
        else:
            proxy = self.bus.get_object(NM_BUS_NAME, device_path)
            self.set_object_property(
                proxy,
                bus_name=NM_DEVICE_IFACE,
                prop_name='Autoconnect',
                value=flag
            )

    # --------------- #
    # Private methods #
    # --------------- #

    def _get_known_device_object_path(self, ifname):
        """
        Returns the device's d-bus object path.
        If the given device name is not known to the system,
        the program will exit with an error message.

        Arguments:
            device_obj_path {string} -- the device's own dbus object path

        Returns:
            dbus.Interface -- dbus interface for the given device
        """
        known_devices = list(map(self._get_device_status, self.all_devices))  # noqa E501
        self.known_device_names = list(map(lambda x: str(x['name']), known_devices))  # noqa E501

        if ifname not in self.known_device_names:
            err_msg = f"""
            [Error]: Could not perform the desired operation on "{ifname}".
            The requested device does not appear to exist.
            """.replace("  ", "")
            raise ValueError(err_msg)

        device_info = next(filter(lambda x: str(x['name']) == ifname, known_devices), None)  # noqa E501
        device_path = device_info['device_path']

        return device_path

    def _get_device_dbus_interface(self, device_obj_path):
        """
        Creates and returns a dbus interface for the device.

        Arguments:
            device_obj_path {string} -- the device's own dbus object path

        Returns:
            dbus.Interface -- dbus interface for the given device
        """
        device_obj = self.bus.get_object(NM_BUS_NAME, device_obj_path)
        device_iface = dbus.Interface(device_obj, NM_DEVICE_IFACE)
        return device_iface

    def _update_connection(self, device_path, ifname):
        """
        Reapplies the settings on the connection
        associated with the given device.

        Arguments:
            device_path {string} -- the device's own dbus object path
            ifname {string} -- the device's interface name
        """
        device = self._get_device_dbus_interface(device_path)
        try:
            device.Reapply({}, 0, 0)
        except DBusException:
            err_msg = f"""
            [Error]: Could not update active connection info for "{ifname}".
            The device is not activated.
            D-Bus object path: ({device_path})
            """.replace("  ", "")
            sys.exit(colored(err_msg, "red"))
        else:
            msg = f'Successfully updated connection information for "{ifname}"'
            click.echo(msg)

    def _disconnect_device(self, device_path, ifname):
        """
        Gets the device's dbus interface and
        calls the Disconnect method on it.
        If an error occurs, the program exits with an error message.

        Arguments:
            device_path {string} -- the device's own dbus object path
            ifname {string} -- the device's name
        """
        device = self._get_device_dbus_interface(device_path)
        try:
            device.Disconnect()
        except DBusException:
            err_msg = f"""
            [Error]: Could not disconnect {ifname}.
            The device is either not active or is already disconnected.
            D-Bus object path: ({device_path})
            """.replace("  ", "")
            sys.exit(colored(err_msg, "red"))
        else:
            click.echo(f'Device "{ifname}" was successfully disconnected')

    def _delete_iface(self, device_path, ifname):
        """
        Gets the device's dbus interface and
        calls the Delete method on it.
        If an error occurs, the program exits with an error message.

        Arguments:
            device_path {string} -- the device's own dbus object path
            ifname {string} -- the device's name
        """
        device = self._get_device_dbus_interface(device_path)
        try:
            device.Delete()
        except DBusException as exc:
            err_msg = exc.get_dbus_message()
            err_msg = f'[Error]: Device - "{ifname}"\n{err_msg}'
            sys.exit(colored(err_msg, "red"))
        else:
            click.echo(f"Successfully deleted {ifname}")

    def _get_device_status(self, obj_path):
        """
        Retrieve general status related information
        about a device.

        Arguments:
            obj_path {string} -- the device's own d-bus object path

        Returns:
            dict -- the device's status information
        """
        dev_props = self.get_all_properties(obj_path, NM_DEVICE_IFACE)
        self._stringify_dbus_values(dev_props)

        dev_name = dev_props.get('Interface', 'Unknown')
        dev_type = dev_props.get('DeviceType', 'Unknown')
        dev_state = dev_props.get('State', 'Unknown')
        dev_conn = dev_props.get('ActiveConnection', '--')

        return {
            'name': dev_name,
            'type':  self.translate_device_type(dev_type),
            'device_status': self.translate_device_state(dev_state),
            'connection': self._get_connection_name(dev_conn),
            'state':  dev_state,
            'connection_path': dev_conn,
            'device_path': obj_path
        }

    def _create_row(self, device_details):
        """
        Maps over the values of `device_details` and
        applies the correct color to each value.

        Arguments:
            device_details {dict} -- the device's *detailed* information (ipv4, dns ...)

        Returns:
            list -- colored values
        """
        state = int(device_details['state'])
        values = device_details.values()
        row_color = self.get_device_state_row_color(state)

        del device_details['device_path']
        del device_details['connection_path']
        del device_details['state']

        return list(map(lambda val: colored(val, row_color), values))

    def _get_connection_name(self, connection_path):
        """
        Retrives the name of the given connection.
        If an error occurs, the program exits with an erorr message.

        Arguments:
            connection_path {string} -- the connection's own d-bus object path

        Returns:
            string -- the connection's name
        """
        try:
            props = self.get_all_properties(
                connection_path,
                NM_ACTIVE_CONN_IFACE
            )
        except DBusException:
            return '--'
        except Exception as e:
            click.echo('An error occured', str(e))
        return props['Id']

    def _stringify_dbus_values(self, _dict):
        # loop through the values and cast them appropriately
        # move that method to WyPy
        map(lambda val: str(val), _dict.values())

    def _get_device_details(self, device_obj, show_all=False):
        """
        Retrives detailed information about the given device.
        By default, the program only returns the status information
        along with an additional 'Mtu' property.
        If the show_all flag is enabled, WyPy will gather even more
        details.

        Arguments:
            device_obj {string} -- the device's own d-bus object path

        Keyword Arguments:
            show_all {bool} -- whether to show all details or not (default: {False})

        Returns:
            dict -- the device's details
        """
        dev_props = self.get_all_properties(device_obj, NM_DEVICE_IFACE)
        self._stringify_dbus_values(dev_props)
        dev_status = self._get_device_status(device_obj)

        general_dev_info = {
            'mtu': dev_props.get('Mtu', 'Unknown'),
        }
        result = dict(dev_status, **general_dev_info)

        if show_all:
            ip4_path = dev_props['Ip4Config']
            ip4props = self.get_all_properties(ip4_path, IP4_CONFIG_IFACE)

            addresses = format_list(ip4props['AddressData'], key='address')
            dns = format_list(ip4props['NameserverData'], key='address')
            gateway = ip4props['Gateway'] if ip4props['Gateway'] != '' else '--'  # noqa E501
            domains = ' / '.join(ip4props['Domains']) if len(ip4props['Domains']) != 0 else '--'  # noqa E501

            ip_info = {
                'ipv4_addresses': addresses,
                'ipv4_dns': dns,
                'ipv4_gateway': gateway,
                'ipv4_domains': domains
            }

            result = dict(result, **ip_info)

        return result

    def _fill_details_table(self, data):
        """
        Iterates over `data`'s items
        Uppercases / colors the key in yellow
        Passes the newly formatted key and its associated value to
        PrettyTable.add_row()

        Arguments:
            data {dict} -- the device's properties
        """
        for k, v in data.items():
            k = format_table_key(k)
            self.details_table.add_row([colored(k, "yellow"), v])
