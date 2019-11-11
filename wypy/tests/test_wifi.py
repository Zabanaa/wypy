from termcolor import colored
from unittest.mock import call
from wypy.utils.constants import DBUS_GENERAL_PROPS


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
