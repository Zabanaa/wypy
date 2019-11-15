from termcolor import colored
from prettytable import PrettyTable
from dbus.exceptions import DBusException
from wypy.utils.constants import (
    NM_BUS_NAME,
    NM_OBJ_PATH,
    DBUS_GENERAL_PROPS,
    NM_IFACE,
    NM_DEVICE_IFACE,
    NM_WIRELESS_IFACE,
    NM_ACCESS_POINT_IFACE
)
from wypy.wypy import WyPy
import sys
import click
import dbus
import time


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
        self.status_table.right_padding_width =  8

    def list_access_points(self):
        click.echo("Scanning for available access points ...")
        wifi_dev_path = self._get_wireless_device_path()
        wifi_dev_obj = self.bus.get_object(NM_BUS_NAME, wifi_dev_path)
        wifi_iface = dbus.Interface(wifi_dev_obj, NM_WIRELESS_IFACE)
        access_points = self._get_all_access_points(wifi_iface)
        rows = list(map(self._create_row, access_points))

        for row in rows:
            self.status_table.add_row(row)

        click.echo(self.status_table)

    def rescan(self):
        click.echo('Performing rescan ...')
        wifi_dev_path = self._get_wireless_device_path()
        wifi_dev_obj = self.bus.get_object(NM_BUS_NAME, wifi_dev_path)
        wifi_iface = dbus.Interface(wifi_dev_obj, NM_WIRELESS_IFACE)
        self._request_scan(wifi_iface)
        click.echo('Done !')

    def turn_on(self):
        click.echo('Enabling WiFi ...')
        wifi_enabled = self._get_wifi_status_code()
        if not wifi_enabled:
            self._enable_wifi()
        else:
            click.echo('WiFi is already enabled. Skipping.')

    def turn_off(self):
        click.echo('Disabling WiFi ...')
        wifi_enabled = self._get_wifi_status_code()
        if wifi_enabled:
            self._disable_wifi()
        else:
            click.echo('WiFi is already disabled. Skipping.')

    def print_status(self):
        status_code = self._get_wifi_status_code()
        prop = DBUS_GENERAL_PROPS[self.wifi_prop]
        status = self.translate_status_code(prop, status_code)
        click.echo(f'WiFi is {status}')

    def _enable_wifi(self):
        self.set_object_property(
            proxy=self.proxy,
            prop_name=self.wifi_prop,
            value=True
        )

    def _disable_wifi(self):
        self.set_object_property(
            proxy=self.proxy,
            prop_name=self.wifi_prop,
            value=False
        )

    def _get_wifi_status_code(self):
        return self.get_object_property(
            proxy=self.proxy,
            prop_name=self.wifi_prop
        )

    def _create_row(self, ap_data):
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
        nm = dbus.Interface(self.proxy, NM_IFACE)
        devices_paths = nm.GetAllDevices()
        all_devices = list(map(lambda dev: self.get_all_properties(dev, NM_DEVICE_IFACE), devices_paths))  # noqa E501
        wireless_devices = list(filter(self._filter_wifi_devices, zip(devices_paths, all_devices)))  # noqa E501

        try:
            wifi_dev_path = wireless_devices[0] 
        except Exception:
            err_msg = '[Error]: No wireless device found'
            sys.exit(colored(err_msg, "red"))
        else:
            return wifi_dev_path[0]

    def _filter_wifi_devices(self, device):
        device_info = device[1]
        real, device_type = device_info['Real'], device_info['DeviceType']
        return bool(real) and True and device_type == 2

    def _get_all_access_points(self, wifi_iface):

        try:
            self._request_scan(wifi_iface)
        except SystemExit:
            time.sleep(4)

        access_points_paths = self._list_ap_paths(wifi_iface)
        access_points = list(map(self._extract_ap_info, access_points_paths))
        return access_points

    def _list_ap_paths(self, wifi_iface):
        return wifi_iface.GetAllAccessPoints()

    def _request_scan(self, wifi_iface):
        try:
            wifi_iface.RequestScan({})
        except DBusException as exc:
            msg = exc.get_dbus_message()
            err = "Scanning not allowed immediately following previous scan"
            if msg == err:
                sys.exit(colored(f"[Error]: {msg}", "red"))

    def _extract_ap_info(self, ap_path):
        props = self.get_all_properties(ap_path, NM_ACCESS_POINT_IFACE)
        return {
            'ssid': self._get_ssid(props.get('Ssid')),
            'mode': self._get_mode(props.get('Mode', '--')),
            'rate': self._format_bitrate(props.get('MaxBitrate')),
            'signal': int(props.get('Strength', '--')),
            'bars': self._get_bars(props.get('Strength'))
        }

    def _get_ssid(self, ssid_byte_list):
        if len(ssid_byte_list) == 0:
            return "--"

        ssid = ""
        for char in ssid_byte_list:
            ssid = ssid + chr(char)

        return ssid

    def _get_bars(self, signal):
        signal = int(signal)
        if signal in range(0, 31):
            return "*"
        elif signal in range(30, 61):
            return "**"
        elif signal in range(60, 81):
            return "***"
        elif signal in range(80, 101):
            return "****"
        else:
            return "--"

    def _get_mode(self, mode):
        mode = int(mode)
        if mode == 4:
            return "Mesh"

        if mode == 3:
            return "Access Point"

        if mode == 2:
            return "Infra"

        if mode == 1:
            return "AdHoc"

        if mode == 0:
            return "Unknown"

    def _format_bitrate(self, bitrate):
        bitrate = int(bitrate) // 1000
        return f"{bitrate} Mbit/s"
