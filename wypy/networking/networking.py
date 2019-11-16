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
        self.connectivity_prop_name = 'Connectivity'

    def get_connectivity_state(self):
        """
        Retrieve general connectivity information from dbus.
        """
        status_code = self._get_connectivity_status_code()
        prop = DBUS_GENERAL_PROPS[self.connectivity_prop_name]
        connectivity_state = self.translate_status_code(prop, status_code)
        self._print_connectivity_state(connectivity_state)

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

    def check_connectivity(self):
        click.echo('Performing connectivity check ...')
        """
        Forces NetworkManager to perform a connectivity check
        """
        status_code = self._check_connectivity_state()
        prop = DBUS_GENERAL_PROPS[self.connectivity_prop_name]
        connectivity_state = self.translate_status_code(prop, status_code)
        self._print_connectivity_state(connectivity_state)

    #   ---------------
    #
    #   Private Methods
    #
    #   ---------------

    def _get_connectivity_status_code(self):
        """
        Retrive the 'Connectivity' property available
        on NetworkManager's main d-bus interface.

        Returns:
            int -- the current network connectivity status code
        """
        status_code = self.get_object_property(
            proxy=self.proxy,
            prop_name=self.connectivity_prop_name
        )
        return int(status_code)

    def _print_connectivity_state(self, status):
        """
        Echo the current connectivity state to the user.

        Arguments:
            status {string} -- the current connectivity status
        """
        click.echo(f'Connectivity state: {status}')

    def _check_connectivity_state(self):
        """
        Calls the CheckConnectivity method on the NetworkManager's
        main d-bus Interface.
        Returns:
            int -- the current networking connectivity state
        """
        state = self.iface.CheckConnectivity()
        return state

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
