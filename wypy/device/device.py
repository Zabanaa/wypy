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

    def print_status(self):
        click.echo('Showing status ...')
        device_paths = self.get_object_property(self.nm, 'AllDevices')
        device_details = list(map(self._get_device_details, device_paths))  # noqa E501
        sorted_details = sorted(device_details, key=lambda k: (k['connection'], k['type']), reverse=True)  # noqa E501
        rows = list(map(self._create_row, sorted_details))

        for row in rows:
            self.status_table.add_row(row)

        click.echo(self.status_table)

    def list_all(self):
        click.echo('list all devices ...')

    def print_details(self, device_name):
        click.echo(f'Showing device details for {device_name}...')

    def _get_device_details(self, obj_path):
        dev_props = self.get_all_properties(obj_path, NM_DEVICE_IFACE)
        map(lambda val: str(val), dev_props.values())

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
