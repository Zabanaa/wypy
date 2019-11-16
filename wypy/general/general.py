import click
from wypy.wypy import WyPy
from wypy.utils.constants import (
    NM_SETTINGS_IFACE,
    NM_SETTINGS_OBJ_PATH,
    NM_OBJ_PATH,
    NM_IFACE,
    DBUS_GENERAL_PROPS
)


class General(WyPy):

    def __init__(self):
        super().__init__()
        self.status_properties = [
            'State', 'Connectivity', 'WirelessEnabled',
            'WirelessHardwareEnabled', 'WwanEnabled',
            'WwanHardwareEnabled'
        ]

    def show_status(self):
        """
        Display the general status of NetworkManager
        """
        status_info = self._get_status_info()
        click.echo('WyPy - General status report \n')
        for prop in status_info:
            name = prop['name']
            status_code = prop['status_code']
            click.echo(f'{name}: {self.translate_status_code(name, status_code)} \n')  # noqa: E501

    def get_hostname(self):
        """
        Get the 'Hostname' property on the main NetworkManager
        d-bus interface and echo it to the user.
        """
        proxy = self.bus.get_object(self.bus_name, NM_SETTINGS_OBJ_PATH)
        hostname = self.get_object_property(
            proxy=proxy,
            bus_name=NM_SETTINGS_IFACE,
            prop_name='Hostname'
        )
        click.echo(f'Hostname: {hostname}')

    #   ---------------
    #
    #   Private Methods
    #
    #   ---------------

    def _get_status_info(self):
        """
        Get all properties available on the main NetworkManager
        dbus interface. Filter only those listed in self.status_properties.

        Returns:
            status_info -- list of dictionaries each containing
            information on the properties listed in self.status_properties.
        """
        props = self.get_all_properties(
            object_path=NM_OBJ_PATH,
            iface_name=NM_IFACE
        )

        status_info = [
            {
                'name': DBUS_GENERAL_PROPS[str(prop)],
                'status_code': int(props[prop])
            }
            for prop in self.status_properties
        ]

        return status_info

