from wypy.utils.constants import NM_BUS_NAME, NM_OBJ_PATH, DBUS_GENERAL_PROPS
from wypy.wypy import WyPy
import click


class WiFi(WyPy):

    def __init__(self):
        super().__init__()
        self.proxy = self.bus.get_object(NM_BUS_NAME, NM_OBJ_PATH)
        self.wifi_prop = 'WirelessEnabled'

    def turn_on(self):
        click.echo('Enabling WiFi ...')
        wifi_enabled = self._get_wifi_status_code()
        if not wifi_enabled:
            self._enable_wifi()
        else:
            click.echo('WiFi is already enabled. Skipping.')

    def turn_off(self):
        click.echo('Disabling WiFi ...')
        wifi_enabled = self._get_wifi_status_code()
        if wifi_enabled:
            self._disable_wifi()
        else:
            click.echo('WiFi is already disabled. Skipping.')

    def print_status(self):
        status_code = self._get_wifi_status_code()
        prop = DBUS_GENERAL_PROPS[self.wifi_prop]
        status = self.translate_status_code(prop, status_code)
        click.echo(f'WiFi is {status}')

    def _enable_wifi(self):
        self.set_object_property(
            proxy=self.proxy,
            prop_name=self.wifi_prop,
            value=True
        )

    def _disable_wifi(self):
        self.set_object_property(
            proxy=self.proxy,
            prop_name=self.wifi_prop,
            value=False
        )

    def _get_wifi_status_code(self):
        return self.get_object_property(
            proxy=self.proxy,
            prop_name=self.wifi_prop
        )
