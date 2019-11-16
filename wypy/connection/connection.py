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
        click.echo('Activating connection ...')
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
        """
        Deactivates a connection.

        Arguments:
            conn {[string]} -- [uuid / name of the connection to delete]
        """
        click.echo('Deactivating connection ...')
        self._get_active_connections()
        filter_key = 'Uuid' if is_valid_uuid(conn) else 'Id'
        conn_ids = [str(c[filter_key]) for c in self.active_connections]

        if conn not in conn_ids:
            sys.exit(f'Could not deactivate {conn}. Connection unknown or inactive.')  # noqa E501
        else:
            conn_to_deactivate = next(filter(lambda x: str(x[filter_key]) == conn, self.active_connections), None)  # noqa E501
            self.nm_iface.DeactivateConnection(conn_to_deactivate['Path'])

    def delete(self, conn):
        """
        Deletes a connection profile.
        If conn is a valid uuid, it will be used to retrieve the connection.
        If not, WyPy will try to filter all known connections
        until it finds a match.
        If no match is found, the program exits with an error message.

        Arguments:
            conn {[string]} -- [uuid / name of the connection to delete]
        """
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
        """
        Echos the list of all available connections to the user.
        """
        click.echo('Showing all connections ...')
        self._get_active_connections()
        connections = self._list_connections_info()

        for conn in connections:
            conn_data = {
                'id': str(conn.get('id', '')),
                'uuid': str(conn.get('uuid', '')),
                'type': conn.get('type', ''),
                'name': str(conn.get('interface-name', '--')),
                'path': conn.get('path', '--')
            }

            if self._is_connection_active(conn_data['uuid']):
                self._color_data(conn_data)

            self.table.add_row(conn_data.values())

        click.echo(self.table)

    def show_active(self):
        """
        Echos the list of active connections to the user.
        """
        click.echo('Showing active connections ...')
        self._get_active_connections()
        conn_values = [conn.values() for conn in self.active_connections]

        for i, vals in enumerate(conn_values):
            conn_values[i] = list(map(lambda val: colored(val, "green"), vals))

        self._print_conns(conn_values)

    #   ---------------
    #
    #   Private Methods
    #
    #   ---------------

    def _get_active_connections(self):
        """
        Retrieves the list of active connection on the system.
        For each active connection found, a dict containing only
        the necessary information is created and appended to
        self.active_connections.
        """
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
        """
        Extract both the name and type of the device associated with
        the given connection.

        Arguments:
            connection_props {[dict]} -- [the connection's properties]

        Returns:
            [tuple] -- [device name and type associated with the connection]
        """
        device_obj = str(connection_props['Devices'][0])
        device_props = self.get_all_properties(device_obj, NM_DEVICE_IFACE)
        return (device_props['Interface'], int(device_props['DeviceType']))

    def _print_conns(self, data):
        """
        Populates self.table with the connection information.
        Displays the table to the user.

        Arguments:
            data {[list]} -- [the list of available connections]
        """
        for row in data:
            self.table.add_row(row)
        click.echo(self.table)

    def _is_connection_active(self, uuid):
        """
        Tests whether or not the given connection is active.
        Arguments:
            uuid {[string]} -- [the uuid of the connection to test]

        Returns:
            [bool] -- [whether the connection is active or not]
        """
        active_conn_uuids = [conn['Uuid'] for conn in self.active_connections]
        return uuid in active_conn_uuids

    def _color_data(self, conn):
        """
        Colors the values of the given connection dictionary.

        Arguments:
            conn {[dict]} -- [the connection whose values are to be colored]
        """
        for key, val in conn.items():
            conn[key] = colored(val, "green")

    def _list_connections_info(self):
        """
        Calls ListConnections available on the settings
        d-bus interface provided by NetworkManager.
        For each connection path, an connection interface is
        created and the GetSettings method is called.
        The 'connection' property is then accessed and assigned to
        a dictionary, which is itself appended to the result list.

        Returns:
            [list] -- [dictionaries containing information
            about the available connections.]
        """
        connections = self.settings_iface.ListConnections()
        result = []

        for conn in connections:
            conn_obj = self.bus.get_object(NM_BUS_NAME, conn)
            conn_iface = dbus.Interface(conn_obj,  NM_CONNECTION_IFACE)
            conn_info = conn_iface.GetSettings()['connection']
            conn_info['path'] = conn
            result.append(conn_info)

        return result
