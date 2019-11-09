from prettytable import PrettyTable
from termcolor import colored
from wypy.wypy import WyPy
from wypy.utils.constants import (
    NM_BUS_NAME,
    NM_OBJ_PATH,
    NM_IFACE,
    NM_DEVICE_IFACE,
    NM_ACTIVE_CONN_IFACE
)
import click
import dbus
from dbus.exceptions import DBusException


class Device(WyPy):

    def __init__(self):
        super().__init__()
        self.nm = self.bus.get_object(NM_BUS_NAME, NM_OBJ_PATH)
        self.nm_iface = dbus.Interface(self.nm, NM_IFACE)
        self.status_table_keys = ['DEVICE', 'TYPE', 'STATE', 'CONNECTION', 'TYPE CODE', 'PATH']
        self.status_table = PrettyTable(self.status_table_keys)
        self.status_table.align = 'l'
        self.all_devices = self.get_object_property(self.nm, 'AllDevices')
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
        click.echo('list all devices ...')
        for device in self.all_devices:
            details = self._get_device_details(device)
            for k, v in details.items():
                self.details_table.add_row([colored(k, "yellow"), v])

            click.echo(self.details_table)
            self.details_table.clear_rows()

    def print_details(self, device_name):
        click.echo(f'Showing device details for {device_name}...')

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
            'connection': self._get_connetion_name(dev_conn),
            'state':  dev_state,
            'connection_path': dev_conn,
        }

    def _create_row(self, device_details):
        state = int(device_details['state'])
        values = device_details.values()
        if state == 100:
            color = "green"
        if state == 30:
            color = "red"
        if state in [10, 20]:
            color = "yellow"
        return list(map(lambda val: colored(val, color), values))

    def _get_connetion_name(self, connection_path):
        try:
            props = self.get_all_properties(
                connection_path,
                NM_ACTIVE_CONN_IFACE
            )
        except DBusException:
            return '--'
        except Exception:
            click.echo('Exception')
        return props['Id']

    def _stringify_dbus_values(self, _dict):
        # loop through the values and cast them appropriately
        # move that method to WyPy
        map(lambda val: str(val), _dict.values())

    def _get_device_details(self, device_obj):
        dev_props = self.get_all_properties(device_obj, NM_DEVICE_IFACE)
        self._stringify_dbus_values(dev_props)
        dev_status = self._get_device_status(device_obj)

        general_dev_info = {
            'mtu': dev_props.get('Mtu', 'Unknown')
        }
        result = dict(dev_status, **general_dev_info)
        return result
