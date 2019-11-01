import click
from wypy.wypy import WyPy
from wypy.utils.constants import (
    NM_SETTINGS_OBJ_PATH,
    NM_SETTINGS_BUS_NAME,
    NM_OBJ_PATH
)


class General(WyPy):

    def __init__(self):
        super().__init__()
        self.status_properties = [
            'State', 'Connectivity', 'WirelessEnabled',
            'WirelessHardwareEnabled', 'WwanEnabled',
            'WwanHardwareEnabled'
        ]
        self.property_names = [
            'STATE', 'CONNECTIVITY',
            'WIFI', 'WIFI-HW', 'WWAN',
            'WWAN-HW'
        ]

    def show_status(self):
        status_info = self._get_status_info()
        click.echo('WyPy - General status report \n')
        for name, status in zip(self.property_names, status_info):
            print(f'{name}: {self._translate_status_code(name, int(status))} \n')  # noqa: E501

    def get_hostname(self):
        proxy = self.bus.get_object(self.bus_name, NM_SETTINGS_OBJ_PATH)
        self.bus_name = NM_SETTINGS_BUS_NAME
        hostname = self.get_object_property(proxy=proxy, prop_name='Hostname')
        click.echo(f'Hostname: {hostname}')

    # private methods
    def _get_status_info(self):
        proxy = self.bus.get_object(self.bus_name, NM_OBJ_PATH)
        status = [
            str(self.get_object_property(proxy=proxy, prop_name=prop))
            for prop in self.status_properties
        ]
        return status
