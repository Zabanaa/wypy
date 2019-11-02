from wypy.wypy import WyPy
from wypy.networking import Network
from wypy.utils.constants import NM_OBJ_PATH, NM_IFACE, NM_BUS_NAME
from termcolor import colored
from dbus.proxies import ProxyObject
import subprocess
import dbus
import dbusmock


def test_get_connectivity_state(network, mocker):
    """
    Assert that Network.get_connectivity_state does the following:
        - calls self.bus.get_object_property
        - calls click.echo with the correct string
    """
    state = 4
    mock_get_prop = mocker.patch.object(WyPy, 'get_object_property', return_value=state)    
    mock_click_echo = mocker.patch('click.echo')
    expected_msg = f'Connectivity State: { colored("full", "green") }'

    network.get_connectivity_state()

    mock_prop_name = mock_get_prop.call_args[1]['prop_name']
    mock_proxy_obj = mock_get_prop.call_args[1]['proxy']

    mock_click_echo.assert_called_once()
    mock_click_echo.assert_called_once_with(expected_msg)

    assert mock_prop_name == 'Connectivity'
    assert isinstance(mock_proxy_obj, ProxyObject)


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


# def test_networking_turn_on(network):
#     """
#         - assert Network.get_networking_status was called
#         - assert Network._enable_networking was called 
#     """
#     pass


# def test_networking_turn_on_error(network):
#     """
#         - assert Network.get_networking_status was called (return 1)
#         - assert click.echo was called with the message
#     """
#     pass


# def test_networking_turn_off(network):
#     """
#         - assert Network.get_networking_status was called
#         - assert Network._disable_networking was called
#     """
#     pass


# def test_networking_turn_off_error(network):
#     """
#         - assert Network.get_networking_status was called (return 0)
#         - assert click.echo was called with the message
#     """
#     pass


# def test_get_networking_status(network):
#     """
#         - assert WyPy.get_object_property was called with 'NetworkingEnabled'
#         passed as an argument along with self.proxy
#     """
#     pass


# # these two tests require that dbus be mocked
# def test_enable_networking(network):
#     pass
#     # network.turn_off()
#     # print(network_manager.stdout.readline())


# def test_disable_networking(network):
#     pass
