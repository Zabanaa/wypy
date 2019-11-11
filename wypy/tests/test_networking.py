from termcolor import colored
from dbus.proxies import ProxyObject


def test_get_connectivity_state(network, mocker):
    """
    Assert that Network.get_connectivity_state does the following:
        - calls self.bus.get_object_property
        - calls click.echo with the correct string
    """
    expected_msg = f'Connectivity State: { colored("full", "green") }'

    get_prop_mock = mocker.patch.object(network, 'get_object_property', return_value=4)
    echo_mock = mocker.patch('click.echo')

    network.get_connectivity_state()

    mock_prop_name = get_prop_mock.call_args[1]['prop_name']
    mock_proxy_obj = get_prop_mock.call_args[1]['proxy']

    echo_mock.assert_called_once()
    echo_mock.assert_called_once_with(expected_msg)

    assert mock_prop_name == 'Connectivity'
    assert isinstance(mock_proxy_obj, ProxyObject)


def test_networking_turn_on(network, mocker):
    """
        - assert Network.get_networking_status was called
        - assert Network._enable_networking was called
    """

    get_status_mock = mocker.patch.object(network, '_get_networking_status', return_value=0)
    enable_network_mock = mocker.patch.object(network, '_enable_networking')

    network.turn_on()
    get_status_mock.assert_called_once()
    enable_network_mock.assert_called_once()


def test_networking_turn_on_error(network, mocker):
    """
        This test case ensures that an error message is printed
        to the user when they attempt to enable networking and
        it's already on.

        - assert Network.get_networking_status was called
        - assert click.echo was called with the expected error message
    """

    echo_mock = mocker.patch('click.echo')
    get_status_mock = mocker.patch.object(network, '_get_networking_status', return_value=1)

    expected_msg = 'Networking is already enabled. Skipping.'
    network.turn_on()
    get_status_mock.assert_called_once()
    echo_mock.assert_called_once_with(expected_msg)

def test_networking_turn_off(network, mocker):
    """
        - assert Network.get_networking_status was called
        - assert Network._disable_networking was called
    """

    get_status_mock = mocker.patch.object(network, '_get_networking_status', return_value=1)
    disable_network_mock = mocker.patch.object(network, '_disable_networking')

    network.turn_off()
    get_status_mock.assert_called_once()
    disable_network_mock.assert_called_once()


def test_networking_turn_off_error(network, mocker):
    """
        - assert Network.get_networking_status was called (return 0)
        - assert click.echo was called with the message
    """
    echo_mock = mocker.patch('click.echo')
    get_status_mock = mocker.patch.object(network, '_get_networking_status', return_value=0)
    expected_msg = 'Networking is already disabled. Skipping.'

    network.turn_off()

    get_status_mock.assert_called_once()
    echo_mock.assert_called_once_with(expected_msg)


def test_get_networking_status(network, mocker):
    """
        - assert WyPy.get_object_property was called with
        'NetworkingEnabled' passed as an argument along
        with self.proxy
    """

    get_prop_mock = mocker.patch.object(network, 'get_object_property')

    network._get_networking_status()
    get_prop_mock.assert_called_once_with(
        prop_name='NetworkingEnabled',
        proxy=network.proxy
    )
