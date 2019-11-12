from wypy.utils.helpers import format_list, format_table_key
from prettytable import PrettyTable
from termcolor import colored
from wypy.wypy import WyPy
from wypy.utils.constants import (
    NM_BUS_NAME,
    NM_OBJ_PATH,
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
        self.all_devices = self.get_object_property(self.nm, 'AllDevices')
        self.known_device_names = []
        self.details_table = PrettyTable(['PROPERTY', 'VALUE'])
        self.details_table.align = 'l'

    def print_status(self):
        click.echo('Showing status ...')
        device_status = list(map(self._get_device_status, self.all_devices))  # noqa E501
        sorted_status = sorted(device_status, key=lambda k: (k['connection'], k['type']), reverse=True)  # noqa E501
        rows = list(map(self._create_row, sorted_status))

        for row in rows:
            self.status_table.add_row(row)

        click.echo(self.status_table)

    def list_all(self):
        click.echo('Listing all devices ...')
        for device in self.all_devices:
            details = self._get_device_details(device)
            self._fill_details_table(details)

            click.echo(self.details_table)
            self.details_table.clear_rows()

    def print_details(self, device_name):
        click.echo(f'Showing device details for {device_name}...')
        known_devices = list(map(self._get_device_status, self.all_devices))  # noqa E501
        self.known_device_names = list(map(lambda x: str(x['name']), known_devices))  # noqa E501

        if device_name not in self.known_device_names:
            err_msg = f'[Error] Could not retrieve details for {device_name}. Device Unknown.'  # noqa E501
            sys.exit(colored(err_msg, "red"))

        _filter = lambda x: str(x['name']) == device_name  # noqa E731
        device_to_show = next(filter(_filter, known_devices), None)
        device_details = self._get_device_details(device_to_show['device_path'], show_all=True)  # noqa E501

        self._fill_details_table(device_details)

        click.echo(self.details_table)

    def update_ifname_connection(self, ifname):
        known_devices = list(map(self._get_device_status, self.all_devices))  # noqa E501
        self.known_device_names = list(map(lambda x: str(x['name']), known_devices))  # noqa E501

        if ifname not in self.known_device_names:
            err_msg = f"""
            [Error]: Could not update "{ifname}".
            The requested device does not appear to exist.
            """.replace("  ", "")
            sys.exit(colored(err_msg, "red"))

        device_to_update = next(filter(lambda x: str(x['name']) == ifname, known_devices), None)
        device_obj_path = device_to_update['device_path']
        self._update_connection(device_obj_path, ifname)

    # --------------- #
    # Private methods #
    # --------------- #

    def _update_connection(self, device_path, ifname):
        device_obj = self.bus.get_object(NM_BUS_NAME, device_path)
        device_iface = dbus.Interface(device_obj, NM_DEVICE_IFACE)
        try:
            device_iface.Reapply({}, 0, 0)
        except DBusException:
            err_msg = f"""
            [Error]: Could not update active connection info for "{ifname}".
            The device is not activated.
            D-Bus object path: ({device_path})
            """.replace("  ", "")
            sys.exit(colored(err_msg, "red"))
        else:
            click.echo(f'Successfully updated active connection information for "{ifname}"')

    def _get_device_status(self, obj_path):
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
        state = int(device_details['state'])
        values = device_details.values()
        row_color = self.get_device_state_row_color(state)

        del device_details['device_path']
        del device_details['connection_path']
        del device_details['state']

        return list(map(lambda val: colored(val, row_color), values))

    def _get_connection_name(self, connection_path):
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
        1. Iterates over `data`'s items
        2. Uppercases / colors the key in yellow
        3. Passes the newly formatted key and its associated value to
           PrettyTable.add_row()
        """
        for k, v in data.items():
            k = format_table_key(k)
            self.details_table.add_row([colored(k, "yellow"), v])
