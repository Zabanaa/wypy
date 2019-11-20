import pytest
import dbus
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

    result = wifi._get_all_access_points()

    request_scan.assert_called_once()
    list_ap_paths.assert_called_once()
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


def test_connect_to_wifi_existing_conn(wifi, mocker):
    dummy_ap_name = 'MyAwesomeAPName'
    dummy_active_conn_path = '/path/to/active/conn'
    dummy_conn_paths = ['/conn/1', '/conn/2']

    list_all_conns = mocker.patch.object(
        wifi,
        '_list_all_connections',
        return_value=dummy_conn_paths
    )

    get_conn_info_mock = mocker.patch.object(
        wifi,
        '_get_connection_info',
        return_value={'id': dummy_ap_name, 'dbus_path': '/path/to/conn/1'}
    )

    prompt_mock = mocker.patch(
        'click.prompt',
        return_value=dummy_ap_name
    )

    echo_mock = mocker.patch('click.echo')

    activate_existing_connection_mock = mocker.patch.object(
        wifi,
        '_activate_existing_connection',
        return_value=dummy_active_conn_path
    )

    wifi.connect()

    success_msg = echo_mock.call_args[0][0]
    list_all_conns.assert_called_once()
    assert get_conn_info_mock.call_count == len(dummy_conn_paths)
    assert prompt_mock.call_count == 2
    activate_existing_connection_mock.assert_called_once_with('/path/to/conn/1')
    assert dummy_active_conn_path and dummy_ap_name in success_msg


# connect not found
def test_connect_to_wifi_non_existant_conn(wifi, mocker):
    dummy_ap_name_and_pwd = 'MyAwesomeAPNameAndPassword'
    dummy_conn_paths = ['/conn/1', '/conn/2']

    list_all_conns = mocker.patch.object(
        wifi,
        '_list_all_connections',
        return_value=dummy_conn_paths
    )

    get_conn_info_mock = mocker.patch.object(
        wifi,
        '_get_connection_info',
        return_value={'id': 'helloworld', 'dbus_path': '/path/to/conn/1'}
    )

    prompt_mock = mocker.patch(
        'click.prompt',
        return_value=dummy_ap_name_and_pwd
    )

    conn_to_ap_mock = mocker.patch.object(
        wifi,
        '_connect_to_access_point'
    )

    wifi.connect()

    list_all_conns.assert_called_once()
    assert get_conn_info_mock.call_count == len(dummy_conn_paths)
    assert prompt_mock.call_count == 2
    conn_to_ap_mock.assert_called_once_with(
        dummy_ap_name_and_pwd,
        dummy_ap_name_and_pwd
    )


def test_connect_to_ap_unknown(wifi, mocker):
    dummy_ap_name = 'some_ap'
    dummy_ap_pass = 'some_pass'
    dummy_aps = [{'ssid': 'hello'}, {'ssid': 'world'}]
    get_all_aps_mock = mocker.patch.object(
        wifi,
        '_get_all_access_points',
        return_value=dummy_aps
    )
    expected_err = "[Error]: Connection to some_ap impossible. No such access point."
    with pytest.raises(SystemExit) as exc:
        wifi._connect_to_access_point(dummy_ap_name, dummy_ap_pass)

    assert colored(expected_err, "red") == exc.value.args[0]
    get_all_aps_mock.assert_called_once()


def test_connect_to_ap(wifi, mocker):
    wifi_conn_info = {'key': 'value'}
    new_conn_uuid = 'new-conn-uuid-v4'
    dummy_ap_name = 'some_ap'
    dummy_ap_pass = 'some_pass'
    dummy_ap_path = '/path/to/ap'
    dummy_aps = [
        {'ssid': dummy_ap_name, 'dbus_path': dummy_ap_path},
        {'ssid': 'world', 'dbus_path': 'some_path_to_dbus'}
    ]
    get_all_aps_mock = mocker.patch.object(
        wifi,
        '_get_all_access_points',
        return_value=dummy_aps
    )
    generate_wifi_info_mock = mocker.patch.object(
        wifi,
        '_generate_wireless_connection_info',
        return_value=wifi_conn_info
    )
    establish_connection_mock = mocker.patch.object(
        wifi,
        '_establish_connection',
        return_value=new_conn_uuid
    )

    wifi._connect_to_access_point(dummy_ap_name, dummy_ap_pass)

    get_all_aps_mock.assert_called_once()
    generate_wifi_info_mock.assert_called_once_with(dummy_ap_name, dummy_ap_pass)
    establish_connection_mock.assert_called_once_with(wifi_conn_info, dummy_ap_path)


def test_generate_wireless_info(wifi):
    dummy_ap = 'some_ap'
    dummy_pw = 'some_pw'
    info = wifi._generate_wireless_connection_info(
        dummy_ap,
        dummy_pw
    )
    expected_keys = [
        'connection', '802-11-wireless',
        '802-11-wireless-security', 'ipv4', 'ipv6'
    ]
    assert isinstance(info, dbus.Dictionary)
    assert sorted(expected_keys) == sorted(info.keys())

    ipv4 = info['ipv4']
    ipv6 = info['ipv6']

    assert 'method' in ipv4.keys()
    assert 'method' in ipv6.keys()
    assert ipv4['method'] == 'auto'
    assert ipv6['method'] == 'ignore'

    security = info['802-11-wireless-security']
    assert sorted(['key-mgmt', 'auth-alg', 'psk']) == sorted(security.keys())
    assert security['key-mgmt'] == 'wpa-psk'
    assert security['auth-alg'] == 'open'
    assert security['psk'] == dummy_pw

    wifi = info['802-11-wireless']
    assert sorted(['ssid', 'mode']) == sorted(wifi.keys())
    assert wifi['ssid'] == dbus.ByteArray(dummy_ap.encode('utf-8'))
    assert wifi['mode'] == 'infrastructure'

    conn = info['connection']
    assert sorted(['type', 'uuid', 'id']) == sorted(conn.keys())
    assert conn['id'] == dummy_ap
    assert conn['type'] == '802-11-wireless'


def test_exit_loop(wifi, mocker):
    quit_loop_mock = mocker.patch.object(wifi.loop, 'quit')
    echo_mock = mocker.patch('click.echo')

    msg = "Done and dusted !"

    wifi._exit_loop(msg)

    echo_mock.assert_called_once_with(msg)
    quit_loop_mock.assert_called_once()


def test_exit_loop_error(wifi, mocker):
    quit_loop_mock = mocker.patch.object(wifi.loop, 'quit')
    echo_mock = mocker.patch('click.echo')

    msg = "Error !!!!"

    wifi._exit_loop(msg, error=True)

    echo_mock.assert_called_once_with(colored(msg, 'red'))
    quit_loop_mock.assert_called_once()


def test_handle_wifi_state_change(wifi, mocker):
    exit_loop_mock = mocker.patch.object(
        wifi,
        '_exit_loop'
    )
    delete_active_conn = mocker.patch.object(
        wifi,
        '_delete_failed_active_connection'
    )

    new_state = 100
    old_state = 30
    reason = 0
    wifi.ap_name = "Some Ap"
    wifi.ap_uuid = "Some UUID"

    msg = f'Connection to {wifi.ap_name} ({wifi.ap_uuid}) successful !'

    wifi._handle_wifi_state_change(new_state, old_state, reason)

    exit_loop_mock.assert_called_once_with(msg)


def test_handle_wifi_state_change_invalid_pwd(wifi, mocker):
    exit_loop_mock = mocker.patch.object(
        wifi,
        '_exit_loop'
    )
    delete_active_conn = mocker.patch.object(
        wifi,
        '_delete_failed_active_connection'
    )

    new_state = 120
    old_state = 70
    reason = 7

    wifi._handle_wifi_state_change(new_state, old_state, reason)

    msg = '[Error]. Could not connect. Invalid Password.'

    delete_active_conn.assert_called_once()
    exit_loop_mock.assert_called_once_with(msg, error=True)


def test_handle_wifi_state_change_error(wifi, mocker):
    exit_loop_mock = mocker.patch.object(
        wifi,
        '_exit_loop'
    )
    delete_active_conn = mocker.patch.object(
        wifi,
        '_delete_failed_active_connection'
    )

    new_state = 120
    old_state = 70
    reason = 9

    wifi._handle_wifi_state_change(new_state, old_state, reason)

    msg = f'[Error] Could not connect. Reason number: {reason}'

    delete_active_conn.assert_called_once()
    exit_loop_mock.assert_called_once_with(msg, error=True)
