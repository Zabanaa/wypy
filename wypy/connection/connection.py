from wypy.utils.helpers import is_valid_uuid
from prettytable import PrettyTable
from termcolor import colored
from wypy.utils.constants import (
    NM_IFACE,
    NM_BUS_NAME,
    NM_OBJ_PATH,
    NM_SETTINGS_IFACE,
    NM_SETTINGS_OBJ_PATH,
    NM_ACTIVE_CONN_IFACE,
    NM_DEVICE_IFACE,
    NM_CONNECTION_IFACE
)
from wypy.wypy import WyPy
import click
import dbus
import sys


class Connection(WyPy):

    def __init__(self):
        super().__init__()
        self.proxy = self.bus.get_object(NM_BUS_NAME, NM_OBJ_PATH)
        self.nm_iface = dbus.Interface(self.proxy, NM_IFACE)
        self.active_conns_prop = 'ActiveConnections'
        self.conn_props = ['Id', 'Uuid', 'Type', 'Devices']
        self.table = PrettyTable(['NAME', 'UUID', 'TYPE', 'DEVICE', 'PATH'])
        self.table.align = 'l'
        self.active_connections = []
        self.settings_obj = self.bus.get_object(NM_BUS_NAME, NM_SETTINGS_OBJ_PATH)  # noqa E501
        self.settings_iface = dbus.Interface(self.settings_obj, NM_SETTINGS_IFACE)  # noqa E501

    def activate(self):
        click.echo('Deactivating connection ...')
        """
            TODO:
                - list all connections
                - get the one that matches the given name
                - find out what device it belongs to
                by calling GetDeviceByIpIface()
                - if no connection matches the given name, exit
                with clear and friendly error message.
        """

    def deactivate(self, conn):
        click.echo('Deactivating connection ...')
        """
            - list active connections
            - if conn_name is not in the list, error out
            - else call DeactivateConnection passing in the path
        """
        self._get_active_connections()
        filter_key = 'Uuid' if is_valid_uuid(conn) else 'Id'
        conn_ids = [str(c[filter_key]) for c in self.active_connections]

        if conn not in conn_ids:
            sys.exit(f'Could not deactivate {conn}. Connection unknown or inactive.')  # noqa E501
        else:
            conn_to_deactivate = next(filter(lambda x: str(x[filter_key]) == conn, self.active_connections), None)  # noqa E501
            self.nm_iface.DeactivateConnection(conn_to_deactivate['Path'])
    
    def delete(self, conn):
        click.echo(f'Deleting connection profile {conn}')
        if is_valid_uuid(conn):
            uuid = conn
        else:
            connections = self._list_connections_info()
            conn_to_delete = next(filter(lambda x: str(x['id']) == conn, connections), None)  # noqa E501
            try:
                uuid = conn_to_delete['uuid']
            except TypeError:
                sys.exit(f'Could not delete {conn}. Connection unknown or already deleted.')

        _conn = self.settings_iface.GetConnectionByUuid(uuid)
        conn_obj = self.bus.get_object(NM_BUS_NAME, _conn)
        conn_obj.Delete(dbus_interface=NM_CONNECTION_IFACE)

    def show_all(self):
        click.echo('Showing all connections ...')
        self._get_active_connections()
        connections = self.settings_iface.ListConnections()

        for conn in connections:
            conn_obj = self.bus.get_object(NM_BUS_NAME, conn)
            conn_iface = dbus.Interface(conn_obj,  NM_CONNECTION_IFACE)
            conn_info = conn_iface.GetSettings()['connection']

            conn_data = {
                'id': str(conn_info.get('id', '')),
                'uuid': str(conn_info.get('uuid', '')),
                'type': conn_info.get('type', ''),
                'name': str(conn_info.get('interface-name', '--')),
                'path': conn
            }

            if self._is_connection_active(conn_data['uuid']):
                self._color_data(conn_data)

            self.table.add_row(conn_data.values())

        click.echo(self.table)

    def show_active(self):
        click.echo('Showing active connections ...')
        self._get_active_connections()
        conn_values = [conn.values() for conn in self.active_connections]

        for i, vals in enumerate(conn_values):
            conn_values[i] = list(map(lambda val: colored(val, "green"), vals))

        self._print_conns(conn_values)

    def _get_active_connections(self):
        active_conns_paths = self.get_object_property(
            proxy=self.proxy,
            prop_name=self.active_conns_prop
        )

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
            conn_props['Path'] = conn

            self.active_connections.append(conn_props)

    def _get_device_info(self, connection_props):
        device_obj = str(connection_props['Devices'][0])
        device_props = self.get_all_properties(device_obj, NM_DEVICE_IFACE)
        return (device_props['Interface'], int(device_props['DeviceType']))

    def _print_conns(self, data):
        for row in data:
            self.table.add_row(row)
        click.echo(self.table)

    def _is_connection_active(self, uuid):
        active_conn_uuids = [conn['Uuid'] for conn in self.active_connections]
        return uuid in active_conn_uuids

    def _color_data(self, conn):
        for key, val in conn.items():
            conn[key] = colored(val, "green")

    def _list_connections_info(self):
        connections = self.settings_iface.ListConnections()
        result = []

        for conn in connections:
            conn_obj = self.bus.get_object(NM_BUS_NAME, conn)
            conn_iface = dbus.Interface(conn_obj,  NM_CONNECTION_IFACE)
            conn_info = conn_iface.GetSettings()['connection']
            conn_info['path'] = conn
            result.append(conn_info)

        return result
