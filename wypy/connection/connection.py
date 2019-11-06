from prettytable import PrettyTable
from termcolor import colored
from wypy.utils.constants import (
    NM_BUS_NAME,
    NM_OBJ_PATH,
    NM_SETTINGS_IFACE,
    NM_SETTINGS_OBJ_PATH,
    NM_ACTIVE_CONN_IFACE,
    NM_DEVICE_IFACE
)
from wypy.wypy import WyPy
import click
import dbus


class Connection(WyPy):

    def __init__(self):
        super().__init__()
        self.proxy = self.bus.get_object(NM_BUS_NAME, NM_OBJ_PATH)
        self.active_conns_prop = 'ActiveConnections'
        self.conn_props = ['Id', 'Uuid', 'Type', 'Devices']

    def activate(self):
        click.echo('Activating connection ...')

    def deactivate(self):
        click.echo('Deactivating connection ...')

    def show_all(self):
        click.echo('Showing all connections ...')
        pass

    def show_one(self):
        click.echo('Connection details: hehe')

    def show_active(self):
        click.echo('Showing active connections ...')
        conns = self._get_active_connections()
        conn_values = [conn.values() for conn in conns]

        for i, vals in enumerate(conn_values):
            conn_values[i] = list(map(lambda val: colored(val, "green"), vals))

        self._print_conns(conn_values)

    def _get_active_connections(self):
        active_conns_paths = self.get_object_property(
            proxy=self.proxy,
            prop_name=self.active_conns_prop
        )

        active_conns_data = []

        for conn in active_conns_paths:
            all_props = self.get_all_properties(conn, NM_ACTIVE_CONN_IFACE)
            conn_props = {
                prop: str(all_props[prop])
                for prop in self.conn_props
                if not isinstance(all_props[prop], dbus.Array)
            }

            device_name, device_type = self._get_device_info(all_props) 
            conn_props['Device'] = device_name
            conn_props['Type'] = self.translate_device_type(device_type)

            active_conns_data.append(conn_props)

        return active_conns_data

    def _get_device_info(self, connection_props):
        device_obj = str(connection_props['Devices'][0])
        device_props = self.get_all_properties(device_obj, NM_DEVICE_IFACE)
        return (device_props['Interface'], int(device_props['DeviceType']))

    def _print_conns(self, data):
        table = PrettyTable(['Name', 'UUID', 'TYPE', 'DEVICE'])
        for row in data:
            table.add_row(row)
        print(table)
