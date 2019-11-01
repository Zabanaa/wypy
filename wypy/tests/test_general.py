from unittest import mock
from dbus.proxies import ProxyObject


def test_show_status(general, mocker):
    """
    Assert that General.show_status effectively makes calls to
    the following private methods:

        _get_status_info
        _translate_status_code

    Both of which are being mocked.
    This test also asserts that _translate_status_code was called 6 times.
    """

    props = general.property_names
    statuses = [70, 4, 1, 1, 1, 1]
    calls = [mock.call(name, status) for name, status in zip(props, statuses)]

    mock_gen = mocker.patch.object(general, '_get_status_info', return_value=statuses)
    mock_translate = mocker.patch.object(general, '_translate_status_code')

    general.show_status()

    mock_translate.assert_has_calls(calls, any_order=True)
    mock_gen.assert_called_once()


def test_get_status_info(general, mocker):
    """
    Assert General.get_status_info calls the get_object_property
    method as many times as there are status_properties,
    each time passing the correct argument.
    """
    mock_get_prop = mocker.patch.object(general, 'get_object_property')

    general._get_status_info()

    proxy_arg = mock_get_prop.call_args[1]['proxy']

    assert mock_get_prop.called == True  # noqa E712
    assert isinstance(proxy_arg, ProxyObject)


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
