from dbus import String as _str
import click
from wypy.wypy import WyPy
from wypy.utils.constants import (
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
        status_info = self._get_status_info()
        click.echo('WyPy - General status report \n')
        for prop in status_info:
            name = prop['name']
            status_code = prop['status_code']
            click.echo(f'{name}: {self.translate_status_code(name, status_code)} \n')  # noqa: E501

    def get_hostname(self):
        proxy = self.bus.get_object(self.bus_name, NM_SETTINGS_OBJ_PATH)
        hostname = self.get_object_property(proxy=proxy, prop_name='Hostname')
        click.echo(f'Hostname: {hostname}')

    # private methods
    def _get_status_info(self):
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

