import pytest
from termcolor import colored
from unittest.mock import call
from wypy.utils.constants import DBUS_GENERAL_PROPS, NM_DEVICE_IFACE


def test_turn_on_wifi(wifi, mocker):
    """
        Assert click.echo was called with the correct message passed
        as the argument.
        Assert WiFi._get_wifi_status_code was called and that if
        it returns 0 (False), Wifi._enable_wifi() is called
    """
    intro_msg = 'Enabling WiFi ...'

    echo_mock = mocker.patch('click.echo')
    get_status_mock = mocker.patch.object(wifi, '_get_wifi_status_code', return_value=0)
    wifi_mock = mocker.patch.object(wifi, '_enable_wifi')

    wifi.turn_on()

    echo_mock.assert_called_once_with(intro_msg)
    get_status_mock.assert_called_once()
    wifi_mock.assert_called_once()


def test_turn_on_wifi_error(wifi, mocker):
    """
        Assert click.echo was called with the correct message passed
        as the argument.
        Assert WiFi._get_wifi_status_code was called and that if
        it returns 1 (True), click.echo is called with the correct
        error message.
    """

    get_status_mock = mocker.patch.object(wifi, '_get_wifi_status_code', return_value=1)
    echo_mock = mocker.patch('click.echo')

    wifi.turn_on()

    expected_err_msg = call('WiFi is already enabled. Skipping.')
    get_status_mock.assert_called_once()
    echo_mock.assert_has_calls([expected_err_msg])


def test_turn_off_wifi(wifi, mocker):
    """
        Assert click.echo was called with the correct message passed
        as the argument.
        Assert WiFi._get_wifi_status_code was called and that if
        it returns 1 (enabled), WiFi._disable_wifi is called.
    """

    get_status_mock = mocker.patch.object(wifi, '_get_wifi_status_code', return_value=1)
    wifi_mock = mocker.patch.object(wifi, '_disable_wifi')
    intro_msg = 'Disabling WiFi ...'
    echo_mock = mocker.patch('click.echo')

    wifi.turn_off()

    echo_mock.assert_called_once_with(intro_msg)
    get_status_mock.assert_called_once()
    wifi_mock.assert_called_once()


def test_turn_off_wifi_error(wifi, mocker):
    """
        Assert click.echo was called with the correct message passed
        as the argument.
        Assert WiFi._get_wifi_status_code was called and that if
        it returns 0 (disabled), click.echo is called with the correct
        error message.
    """
    get_status_mock = mocker.patch.object(wifi, '_get_wifi_status_code', return_value=0)
    echo_mock = mocker.patch('click.echo')
    expected_err_msg = call('WiFi is already disabled. Skipping.')

    wifi.turn_off()

    get_status_mock.assert_called_once()
    echo_mock.assert_has_calls([expected_err_msg])


def test_print_wifi_status(wifi, mocker):
    """
        Assert Wifi.print_status() correctly retrieves the current
        wireless state, translates it to a colored string and outputs
        the correct message to the user.
    """
    get_status_mock = mocker.patch.object(wifi, '_get_wifi_status_code', return_value=1)
    echo_mock = mocker.patch('click.echo')
    translate_mock = mocker.patch.object(wifi, 'translate_status_code', return_value=colored("enabled", "green"))

    wifi_prop = DBUS_GENERAL_PROPS[wifi.wifi_prop]

    wifi.print_status()

    expected_output = f'WiFi is {colored("enabled", "green")}'
    get_status_mock.assert_called_once()
    translate_mock.assert_called_once_with(wifi_prop, 1)
    echo_mock.assert_called_once_with(expected_output)


def test_enable_wifi(wifi, mocker):
    """
        Assert Wifi._enable_wifi() calls its inherited
        set_object_property method passing it the correct
        proxy, prop name and value (True in this case).
    """
    set_prop_mock = mocker.patch.object(wifi, 'set_object_property')
    wifi._enable_wifi()

    set_prop_mock.assert_called_once_with(
        proxy=wifi.proxy,
        prop_name=wifi.wifi_prop,
        value=True
    )


def test_disable_wifi(wifi, mocker):
    """
        Assert Wifi._disable_wifi() calls its inherited
        set_object_property method passing it the correct
        proxy, prop name and value (False in this case).
    """
    set_prop_mock = mocker.patch.object(wifi, 'set_object_property')

    wifi._disable_wifi()

    set_prop_mock.assert_called_once_with(
        proxy=wifi.proxy,
        prop_name=wifi.wifi_prop,
        value=False
    )


def test_get_wifi_status_code(wifi, mocker):
    get_prop_mock = mocker.patch.object(wifi, 'get_object_property')
    wifi._get_wifi_status_code()
    get_prop_mock.assert_called_once_with(
        proxy=wifi.proxy,
        prop_name=wifi.wifi_prop
    )


# TODO:
def test_format_bitrate(wifi):
    bitrate = 134000.00
    result = wifi._format_bitrate(bitrate)
    assert result == '134 Mbit/s'


def test_get_mode(wifi):
    mode = '4'
    result = wifi._get_mode(mode)
    assert result == 'Mesh'

    mode = '3'
    result = wifi._get_mode(mode)
    assert result == 'Access Point'

    mode = '2'
    result = wifi._get_mode(mode)
    assert result == 'Infra'

    mode = '1'
    result = wifi._get_mode(mode)
    assert result == 'Ad Hoc'

    mode = '0'
    result = wifi._get_mode(mode)
    assert result == 'Unknown'


def test_get_bars(wifi):
    signal = '2'
    result = wifi._get_bars(signal)
    assert result == '*'

    signal = '41'
    result = wifi._get_bars(signal)
    assert result == '**'

    signal = '71'
    result = wifi._get_bars(signal)
    assert result == '***'

    signal = '100'
    result = wifi._get_bars(signal)
    assert result == '****'

    signal = '23420'
    result = wifi._get_bars(signal)
    assert result == '--'


def test_get_ssid(wifi):
    raw_ssid = [0x50, 0x61, 0x72, 0x69, 0x73, 0x20, 0x57, 0x69, 0x2d, 0x46, 0x69]
    result = wifi._get_ssid(raw_ssid)
    assert result == "Paris Wi-Fi"

    raw_ssid = []
    result = wifi._get_ssid(raw_ssid)
    assert result == '--'


def test_extract_access_point_info(wifi, mocker):
    access_point_props = {
        'hello': 'world',
        'temperature': 80,
        'fragile': False,
        'Ssid': [],
        'Mode': '2',
        'MaxBitrate': '982909',
        'Strength': '92',
        'name': 'Karim Benzema',
        'age': 32,
        'current_club': 'Real Madrid CF'
    }
    expected_keys = [
        'ssid', 'mode', 'rate',
        'signal', 'bars', 'dbus_path'
    ]
    get_all_props_mock = mocker.patch.object(
        wifi,
        'get_all_properties',
        return_value=access_point_props
    )

    result = wifi._extract_ap_info('/some/path')

    get_all_props_mock.assert_called_once()
    assert sorted(expected_keys) == sorted(result.keys())


def test_get_all_access_points(wifi, mocker):
    dummy_ap_paths = ['/ap/1', '/ap/2', '/ap/3']
    request_scan = mocker.patch.object(wifi, '_request_scan')
    list_ap_paths = mocker.patch.object(
        wifi,
        '_list_ap_paths',
        return_value=dummy_ap_paths
    )
    extract_ap_info = mocker.patch.object(
        wifi,
        '_extract_ap_info',
        return_value={'name': 'Karim Benzema', 'club': 'Real Madrid CF'}
    )
    dummy_iface = 'dummy_iface'
    dummy_ap_paths_calls = [call(path) for path in dummy_ap_paths]

    result = wifi._get_all_access_points(dummy_iface)

    request_scan.assert_called_once_with(dummy_iface)
    list_ap_paths.assert_called_once_with(dummy_iface)
    extract_ap_info.assert_has_calls(dummy_ap_paths_calls)
    assert isinstance(result, list) == True


def test_filter_wifi_devices(wifi):
    device = ('/dev/path', {'Real': 1, 'DeviceType': 2})
    result = wifi._is_device_wifi(device)
    assert result == True

    device = ('/dev/path', {'Real': 0, 'DeviceType': 7623})
    result = wifi._is_device_wifi(device)
    assert result == False


def test_get_wireless_device_path(wifi, mocker):
    dummy_devices = ['/dev/1', '/dev/2']
    get_all_dev_paths = mocker.patch.object(
        wifi,
        '_get_all_devices_paths',
        return_value=dummy_devices
    )
    get_all_props = mocker.patch.object(
        wifi,
        'get_all_properties',
        return_value={}
    )
    is_device_wifi = mocker.patch.object(
        wifi,
        '_is_device_wifi',
        return_value=True
    )

    get_all_props_calls = [call(dev, NM_DEVICE_IFACE) for dev in dummy_devices]
    is_device_wifi_calls = [call((dev, {})) for dev in dummy_devices]

    result = wifi._get_wireless_device_path()

    get_all_dev_paths.assert_called_once()
    get_all_props.assert_has_calls(get_all_props_calls)
    is_device_wifi.assert_has_calls(is_device_wifi_calls)

    assert result == '/dev/1'

# TODO
# connect 
# connect not found

# _get_connection_info
# _activate_existing_connection
# _generate_wireless_connection_info
# _establish_wireless_connection
# _connect_to_access_point