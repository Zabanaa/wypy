from unittest.mock import patch
from wypy.wypy import WyPy
from wypy.networking import Network
from wypy.utils.constants import NM_OBJ_PATH, NM_IFACE, NM_BUS_NAME
from termcolor import colored
from dbus.proxies import ProxyObject
import subprocess
import dbus
import dbusmock


class TestNetworking(dbusmock.DBusTestCase):

    @classmethod
    def setUpClass(cls):
        cls.start_system_bus()
        cls.dbus_con = cls.get_dbus(system_bus=True)

    def setUp(self):
        self.p_mock = self.spawn_server(
            NM_BUS_NAME,
            NM_OBJ_PATH,
            NM_IFACE,
            system_bus=True,
            stdout=subprocess.PIPE
        )

        proxy_obj = self.dbus_con.get_object(NM_BUS_NAME, NM_OBJ_PATH)
        self.nm_iface_mock = dbus.Interface(proxy_obj, dbusmock.MOCK_IFACE)
        self.nm_iface_mock.AddMethod('', 'Enable', '', '', '')
        self.network = Network()

    def tearDown(self):
        self.p_mock.terminate()
        self.p_mock.wait()

    @patch.object(WyPy, 'get_object_property', return_value=4)
    @patch('click.echo')
    def test_get_connectivity_state(self, echo_mock, wypy_mock):
        """
        Assert that Network.get_connectivity_state does the following:
            - calls self.bus.get_object_property
            - calls click.echo with the correct string
        """
        expected_msg = f'Connectivity State: { colored("full", "green") }'

        self.network.get_connectivity_state()

        mock_prop_name = wypy_mock.call_args[1]['prop_name']
        mock_proxy_obj = wypy_mock.call_args[1]['proxy']

        echo_mock.assert_called_once()
        echo_mock.assert_called_once_with(expected_msg)

        assert mock_prop_name == 'Connectivity'
        assert isinstance(mock_proxy_obj, ProxyObject)

    @patch.object(Network, '_get_networking_status', return_value=0)
    @patch.object(Network, '_enable_networking')
    def test_networking_turn_on(self, get_status_mock, enable_network_mock):
        """
            - assert Network.get_networking_status was called
            - assert Network._enable_networking was called
        """
        self.network.turn_on()
        get_status_mock.assert_called_once()
        enable_network_mock.assert_called_once()

    @patch.object(Network, '_get_networking_status', return_value=1)
    @patch('click.echo')
    def test_networking_turn_on_error(self, echo_mock, get_status_mock):
        """
            This test case ensures that an error message is printed
            to the user when they attempt to enable networking and
            it's already on.

            - assert Network.get_networking_status was called
            - assert click.echo was called with the expected error message
        """
        expected_msg = 'Networking is already enabled. Skipping.'
        self.network.turn_on()
        get_status_mock.assert_called_once()
        echo_mock.assert_called_once_with(expected_msg)

    @patch.object(Network, '_get_networking_status', return_value=1)
    @patch.object(Network, '_disable_networking')
    def test_networking_turn_off(self, get_status_mock, disable_network_mock):
        """
            - assert Network.get_networking_status was called
            - assert Network._disable_networking was called
        """
        self.network.turn_off()
        get_status_mock.assert_called_once()
        disable_network_mock.assert_called_once()

    @patch.object(Network, '_get_networking_status', return_value=0)
    @patch('click.echo')
    def test_networking_turn_off_error(self, echo_mock, get_status_mock):
        """
            - assert Network.get_networking_status was called (return 0)
            - assert click.echo was called with the message
        """
        expected_msg = 'Networking is already disabled. Skipping.'
        self.network.turn_off()
        get_status_mock.assert_called_once()
        echo_mock.assert_called_once_with(expected_msg)

    @patch.object(Network, 'get_object_property')
    def test_get_networking_status(self, get_prop_mock):
        """
            - assert WyPy.get_object_property was called with
            'NetworkingEnabled' passed as an argument along
            with self.proxy
        """
        self.network._get_networking_status()
        get_prop_mock.assert_called_once_with(
            prop_name='NetworkingEnabled',
            proxy=self.network.proxy
        )
