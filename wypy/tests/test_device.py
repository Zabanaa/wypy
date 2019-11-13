import pytest
from termcolor import colored
from dbus.exceptions import DBusException
from unittest.mock import call
from wypy.utils.constants import NM_BUS_NAME, NM_DEVICE_IFACE

fmt_mock_path = 'wypy.device.device.format_table_key'
colored_mock_path = 'wypy.device.device.colored'


def test_fill_details_table(device, mocker):

    data = {
        'name': 'karim',
        'location': 'paris',
        'player': 'benzema',
        'birth_place': 'lyon'
    }
    table = device.details_table
    fmt_mock = mocker.patch(fmt_mock_path)
    colored_mock = mocker.patch(colored_mock_path)
    add_row_mock = mocker.patch.object(table, 'add_row')

    device._fill_details_table(data)

    fmt_mock_call_args = [call(k) for k in data.keys()]

    fmt_mock.assert_has_calls(fmt_mock_call_args, any_order=True)
    assert len(colored_mock.call_args_list) == len(data.values())
    assert len(add_row_mock.call_args_list) == len(data.values())


def test_get_device_details(device, mocker):
    all_props_mock = mocker.patch.object(device, 'get_all_properties')
    str_dbus_vals_mock = mocker.patch.object(device, '_stringify_dbus_values')
    dev_status_mock = mocker.patch.object(device, '_get_device_status')

    result = device._get_device_details('some_obj_path')

    assert all_props_mock.called_once()
    assert str_dbus_vals_mock.called_once()
    assert dev_status_mock.called_once()

    assert isinstance(result, dict)
    assert 'mtu' in result.keys()


def test_get_device_details_show_all(device, mocker):
    all_props_mock = mocker.patch.object(device, 'get_all_properties')
    str_dbus_vals_mock = mocker.patch.object(device, '_stringify_dbus_values')
    dev_status_mock = mocker.patch.object(device, '_get_device_status')
    expected_keys = ['mtu', 'ipv4_addresses', 'ipv4_domains', 'ipv4_dns', 'ipv4_gateway']

    result = device._get_device_details('some_obj_path', show_all=True)

    assert all_props_mock.called_once()
    assert str_dbus_vals_mock.called_once()
    assert dev_status_mock.called_once()

    assert isinstance(result, dict)
    assert sorted(expected_keys) == sorted(result.keys())


def test_get_connection_name(device, mocker):
    conn_name = 'my_conn_name'
    all_props_mock = mocker.patch.object(
        device,
        'get_all_properties',
        return_value={'Id': conn_name}
    )
    result = device._get_connection_name('some_connection_path')

    all_props_mock.assert_called_once()
    assert result == conn_name


def test_get_connection_name_exc(device, mocker):
    echo_mock = mocker.patch('click.echo')
    with pytest.raises(Exception):
        device._get_connection_name('some_conn_path')
    echo_mock.assert_called_once()


def test_create_row(device, mocker):
    row_color_mock = mocker.patch.object(
        device, 
        'get_device_state_row_color',
        return_value="green"
    )

    state = 10

    data = {
        'name': 'karim',
        'location': 'paris',
        'player': 'benzema',
        'birth_place': 'lyon',
        'device_path': 'hello',
        'connection_path': 'hello',
        'state': state
    }

    initial_values = len(data.values())

    result = device._create_row(data)

    row_color_mock.assert_called_once_with(10)

    assert len(result) == initial_values - 3


def test_get_device_status(device, mocker):
    all_props_mock = mocker.patch.object(device, 'get_all_properties')
    str_dbus_vals_mock = mocker.patch.object(device, '_stringify_dbus_values')
    conn_name_mock = mocker.patch.object(device, '_get_connection_name')
    translate_dev_state = mocker.patch.object(device, 'translate_device_state')
    translate_dev_type = mocker.patch.object(device, 'translate_device_type')

    expected_keys = [
        'name', 'type',
        'device_status', 'connection',
        'state', 'connection_path', 'device_path'
    ]
    result = device._get_device_status('some_object_path')

    all_props_mock.assert_called_once()
    str_dbus_vals_mock.assert_called_once()
    conn_name_mock.assert_called_once()
    translate_dev_type.assert_called_once()
    translate_dev_state.assert_called_once()

    assert sorted(result.keys()) == sorted(expected_keys)


def test_print_status(device, mocker):
    echo_mock = mocker.patch('click.echo')
    add_row_mock = mocker.patch.object(device.status_table, 'add_row')
    dev_status_mock = mocker.patch.object(device, '_get_device_status')
    create_row_mock = mocker.patch.object(
        device,
        '_create_row',
        return_value=['hello', 'world', 'liverpool', 'mancity']
    )
    device.all_devices = ['/dev/1', '/dev/2', '/dev/3']

    device.print_status()

    assert len(echo_mock.call_args_list) == 2
    assert len(add_row_mock.call_args_list) == len(device.all_devices)
    assert len(create_row_mock.call_args_list) == len(device.all_devices)
    assert len(dev_status_mock.call_args_list) == len(device.all_devices)


def test_list_all(device, mocker):
    dev_details_mock = mocker.patch.object(device, '_get_device_details')
    fill_details_mock = mocker.patch.object(device, '_fill_details_table')
    echo_mock = mocker.patch('click.echo')
    clear_rows_mock = mocker.patch.object(device.details_table, 'clear_rows')

    device.all_devices = ['/dev/1', '/dev/2', '/dev/3']

    device.list_all()

    assert len(echo_mock.call_args_list) == len(device.all_devices) + 1
    assert len(clear_rows_mock.call_args_list) == len(device.all_devices)
    assert len(dev_details_mock.call_args_list) == len(device.all_devices)
    assert len(fill_details_mock.call_args_list) == len(device.all_devices)


def test_manage_device_on(device, mocker):
    dummy_path = '/some/path/to/device'
    dummy_iface = 'dummy0'
    dummy_obj = 'some_obj'
    dev_path_mock = mocker.patch.object(
        device,
        '_get_known_device_object_path',
        return_value=dummy_path
    )
    get_obj_mock = mocker.patch.object(
        device.bus,
        'get_object',
        return_value=dummy_obj

    )
    set_prop_mock = mocker.patch.object(device, 'set_object_property')

    device.manage(dummy_iface)

    dev_path_mock.assert_called_once_with(dummy_iface)
    get_obj_mock.assert_called_once_with(NM_BUS_NAME, dummy_path)
    set_prop_mock.assert_called_once_with(
        dummy_obj,
        bus_name=NM_DEVICE_IFACE,
        prop_name='Managed',
        value=True
    )


def test_manage_device_off(device, mocker):
    dummy_path = '/some/path/to/device'
    dummy_iface = 'dummy0'
    dummy_obj = 'some_obj'
    dev_path_mock = mocker.patch.object(
        device,
        '_get_known_device_object_path',
        return_value=dummy_path
    )
    get_obj_mock = mocker.patch.object(
        device.bus,
        'get_object',
        return_value=dummy_obj

    )
    set_prop_mock = mocker.patch.object(device, 'set_object_property')

    device.manage(dummy_iface, flag=False)

    dev_path_mock.assert_called_once_with(dummy_iface)
    get_obj_mock.assert_called_once_with(NM_BUS_NAME, dummy_path)
    set_prop_mock.assert_called_once_with(
        dummy_obj,
        bus_name=NM_DEVICE_IFACE,
        prop_name='Managed',
        value=False
    )


def test_manage_device_unknown(device, mocker):
    device.known_device_names = ['/dev/1', '/dev/2', '/dev/3']
    dummy_iface = 'unknown_iface'

    with pytest.raises(SystemExit) as exc:
        device.manage(dummy_iface)

    assert dummy_iface in str(exc.value)


def test_autoconnect_device_on(device, mocker):
    dummy_path = '/some/path/to/device'
    dummy_iface = 'dummy0'
    dummy_obj = 'some_obj'
    dev_path_mock = mocker.patch.object(
        device,
        '_get_known_device_object_path',
        return_value=dummy_path
    )
    get_obj_mock = mocker.patch.object(
        device.bus,
        'get_object',
        return_value=dummy_obj

    )
    set_prop_mock = mocker.patch.object(device, 'set_object_property')

    device.autoconnect(dummy_iface)

    dev_path_mock.assert_called_once_with(dummy_iface)
    get_obj_mock.assert_called_once_with(NM_BUS_NAME, dummy_path)
    set_prop_mock.assert_called_once_with(
        dummy_obj,
        bus_name=NM_DEVICE_IFACE,
        prop_name='Autoconnect',
        value=True
    )


def test_autoconnect_device_off(device, mocker):
    dummy_path = '/some/path/to/device'
    dummy_iface = 'dummy0'
    dummy_obj = 'some_obj'
    dev_path_mock = mocker.patch.object(
        device,
        '_get_known_device_object_path',
        return_value=dummy_path
    )
    get_obj_mock = mocker.patch.object(
        device.bus,
        'get_object',
        return_value=dummy_obj

    )
    set_prop_mock = mocker.patch.object(device, 'set_object_property')

    device.autoconnect(dummy_iface, flag=False)

    dev_path_mock.assert_called_once_with(dummy_iface)
    get_obj_mock.assert_called_once_with(NM_BUS_NAME, dummy_path)
    set_prop_mock.assert_called_once_with(
        dummy_obj,
        bus_name=NM_DEVICE_IFACE,
        prop_name='Autoconnect',
        value=False
    )


def test_autoconnect_device_unknown(device, mocker):
    device.known_device_names = ['/dev/1', '/dev/2', '/dev/3']
    dummy_iface = 'unknown_iface'

    with pytest.raises(SystemExit) as exc:
        device.autoconnect(dummy_iface)

    assert dummy_iface in str(exc.value)


def test_disconnect_device(device, mocker):
    dummy_iface = 'some_iface'
    dummy_path = '/some/path/to/device'
    dev_path_mock = mocker.patch.object(
        device,
        '_get_known_device_object_path',
        return_value=dummy_path
    )
    disconnect_mock = mocker.patch.object(device, '_disconnect_device')

    device.disconnect(dummy_iface)

    dev_path_mock.assert_called_once_with(dummy_iface)
    disconnect_mock.assert_called_once_with(dummy_path, dummy_iface)


def test_disconnect_device_unknown(device, mocker):
    device.known_device_names = ['/dev/1', '/dev/2', '/dev/3']
    dummy_iface = 'unknown_iface'

    with pytest.raises(SystemExit) as exc:
        device.disconnect(dummy_iface)

    assert dummy_iface in str(exc.value)


def test_update_device(device, mocker):
    dummy_iface = 'some_iface'
    dummy_path = '/some/path/to/device'
    dev_path_mock = mocker.patch.object(
        device,
        '_get_known_device_object_path',
        return_value=dummy_path
    )

    update_mock = mocker.patch.object(device, '_update_connection')

    device.update_ifname_connection(dummy_iface)

    dev_path_mock.assert_called_once_with(dummy_iface)
    update_mock.assert_called_once_with(dummy_path, dummy_iface)


def test_update_device_unknown(device, mocker):
    device.known_device_names = ['/dev/1', '/dev/2', '/dev/3']
    dummy_iface = 'unknown_iface'

    with pytest.raises(SystemExit) as exc:
        device.update_ifname_connection(dummy_iface)

    assert dummy_iface in str(exc.value)


def test_delete_device(device, mocker):
    dummy_iface = 'some_iface'
    dummy_path = '/some/path/to/device'
    dev_path_mock = mocker.patch.object(
        device,
        '_get_known_device_object_path',
        return_value=dummy_path
    )

    delete_mock = mocker.patch.object(device, '_delete_iface')

    device.delete_iface(dummy_iface)

    dev_path_mock.assert_called_once_with(dummy_iface)
    delete_mock.assert_called_once_with(dummy_path, dummy_iface)


def test_delete_device_unknown(device, mocker):
    device.known_device_names = ['/dev/1', '/dev/2', '/dev/3']
    dummy_iface = 'unknown_iface'

    with pytest.raises(SystemExit) as exc:
        device.delete_iface(dummy_iface)

    assert dummy_iface in str(exc.value)


# def test_disconnect_device_already_down(device, mocker):
#     """need dbus for that one"""
#     pass
