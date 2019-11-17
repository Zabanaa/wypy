from unittest import mock
from unittest.mock import call
from dbus.proxies import ProxyObject
from wypy.utils.constants import (
    DBUS_GENERAL_PROPS,
    NM_OBJ_PATH,
    NM_IFACE
)


def test_show_status(general, mocker):
    """
    Assert that General.show_status effectively makes calls to
    the following private methods:

        _get_status_info
        translate_status_code

    Both of which are being mocked.
    This test also asserts that translate_status_code was called 6 times.
    """

    prop_names = DBUS_GENERAL_PROPS.values()
    status_codes = [70, 4, 1, 1, 1, 1]
    calls = [
        call(name, status)
        for name, status in zip(prop_names, status_codes)
    ]
    info = [
        {'name': name, 'status_code': status}
        for name, status in zip(prop_names, status_codes)
    ]

    echo_mock = mocker.patch('click.echo')
    mock_info = mocker.patch.object(general, '_get_status_info', return_value=info)
    mock_translate = mocker.patch.object(general, 'translate_status_code')

    general.show_status()

    assert len(echo_mock.call_args_list) == len(info) + 1
    mock_info.assert_called_once()
    mock_translate.assert_has_calls(calls, any_order=True)

def test_get_status_info(general, mocker):
    """
    Assert General.get_status_info calls the get_object_property
    method as many times as there are status_properties,
    each time passing the correct argument.
    """
    mock_get_prop = mocker.patch.object(general, 'get_all_properties')

    general._get_status_info()

    expected_call = call(iface_name=NM_IFACE, object_path=NM_OBJ_PATH)

    assert mock_get_prop.call_args == expected_call



def test_get_hostname(general, mocker):
    """
    Assert General.get_hostname calls the get_object_property method
    with 'Hostname' as the argument.
    """
    dbus_prop_name = 'Hostname'
    mock_hostname = 'some hostname'

    mock_get_prop = mocker.patch.object(general, 'get_object_property', return_value=mock_hostname)
    mock_click_echo = mocker.patch('click.echo')

    general.get_hostname()

    prop_arg = mock_get_prop.call_args[1]['prop_name']

    mock_click_echo.assert_called_once_with(f'Hostname: {mock_hostname}')
    assert prop_arg == dbus_prop_name
