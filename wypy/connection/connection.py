from wypy.utils.constants import (
    NM_BUS_NAME,
    NM_OBJ_PATH,
    NM_SETTINGS_IFACE,
    NM_SETTINGS_OBJ_PATH,
    NM_ACTIVE_CONN_IFACE
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
        for conn in conns:
            print(conn['Id'], conn['Uuid'], conn['Type'], conn['Device'])

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

            ## get device name (IF THERE'S A DEVICE SHOW IT ELSE PRINT '--')
            conn_props['Device'] = str(all_props['Devices'][0])
            active_conns_data.append(conn_props)
        
        return active_conns_data
