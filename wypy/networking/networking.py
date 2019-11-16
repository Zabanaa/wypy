import click
import dbus
from wypy.wypy import WyPy
from wypy.utils.constants import (
    DBUS_GENERAL_PROPS,
    NM_IFACE,
    NM_OBJ_PATH,
    NM_BUS_NAME
)


class Network(WyPy):

    def __init__(self):
        super().__init__()
        self.proxy = self.bus.get_object(NM_BUS_NAME, NM_OBJ_PATH)
        self.iface = dbus.Interface(self.proxy, NM_IFACE)

    def get_connectivity_state(self):
        """
        Retrieve general connectivity information from dbus.
        """
        prop_name = 'Connectivity'
        status_code = self.get_object_property(
            proxy=self.proxy,
            prop_name=prop_name
        )
        prop = DBUS_GENERAL_PROPS[prop_name]
        status_str = self.translate_status_code(prop, status_code)
        click.echo(f'Connectivity State: {status_str}')

    def turn_on(self):
        """
        Enable networking on NetworkManager.
        A check is performed before hand.
        WyPy will exit with an error message if networking is already enabled.
        """
        networking_enabled = self._get_networking_status()
        if not networking_enabled:
            self._enable_networking()
        else:
            click.echo('Networking is already enabled. Skipping.')

    def turn_off(self):
        """
        Disable networking on NetworkManager.
        A check is performed before hand.
        WyPy will exit with an error message if networking is already disabled.
        """
        networking_enabled = self._get_networking_status()
        if networking_enabled:
            self._disable_networking()
        else:
            click.echo('Networking is already disabled. Skipping.')

    #   ---------------
    #
    #   Private Methods
    #
    #   ---------------

    def _enable_networking(self):
        """
        Calls the `Enable` method available on the main
        NetworkManager d-bus interface.

        interface: org.freedesktop.NetworkManager
        """
        self.iface.Enable(True)

    def _disable_networking(self):
        """
        Calls the `Disable` method available on the main
        NetworkManager d-bus interface.

        interface: org.freedesktop.NetworkManager
        """
        self.iface.Enable(False)

    def _get_networking_status(self):
        """
        Retrieve the `NetworingEnabled` property on the main
        NetworkManager d-bus Interface.

        Returns:
            [int] -- [the networking status code]
        """
        status_code = self.get_object_property(
            proxy=self.proxy,
            prop_name='NetworkingEnabled'
        )
        return int(status_code)
