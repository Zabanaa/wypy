from unittest.mock import patch, call
from wypy.wifi import WiFi
from wypy.utils.constants import (
    NM_OBJ_PATH,
    NM_IFACE,
    NM_BUS_NAME,
    DBUS_GENERAL_PROPS
)
from termcolor import colored
import subprocess
import dbus
import dbusmock


class TestWiFi(dbusmock.DBusTestCase):

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
        # call AddMethod here
        self.wifi = WiFi()

    def tearDown(self):
        self.p_mock.terminate()
        self.p_mock.wait()

    @patch.object(WiFi, '_enable_wifi')
    @patch.object(WiFi, '_get_wifi_status_code', return_value=0)
    @patch('click.echo')
    def test_turn_on_wifi(self, echo_mock, get_status_mock, wifi_mock):
        """
            Assert click.echo was called with the correct message passed
            as the argument.
            Assert WiFi._get_wifi_status_code was called and that if
            it returns 0 (False), Wifi._enable_wifi() is called
        """
        intro_msg = 'Enabling WiFi ...'
        self.wifi.turn_on()
        echo_mock.assert_called_once_with(intro_msg)
        get_status_mock.assert_called_once()
        wifi_mock.assert_called_once()

    @patch.object(WiFi, '_enable_wifi')
    @patch.object(WiFi, '_get_wifi_status_code', return_value=1)
    @patch('click.echo')
    def test_turn_on_wifi_error(self, echo_mock, get_status_mock, wifi_mock):
        """
            Assert click.echo was called with the correct message passed
            as the argument.
            Assert WiFi._get_wifi_status_code was called and that if
            it returns 1 (True), click.echo is called with the correct
            error message.
        """
        self.wifi.turn_on()
        expected_err_msg = call('WiFi is already enabled. Skipping.')
        get_status_mock.assert_called_once()
        echo_mock.assert_has_calls([expected_err_msg])

    @patch.object(WiFi, '_disable_wifi')
    @patch.object(WiFi, '_get_wifi_status_code', return_value=1)
    @patch('click.echo')
    def test_turn_off_wifi(self, echo_mock, get_status_mock, wifi_mock):
        """
            Assert click.echo was called with the correct message passed
            as the argument.
            Assert WiFi._get_wifi_status_code was called and that if
            it returns 1 (enabled), WiFi._disable_wifi is called.
        """
        self.wifi.turn_off()
        intro_msg = 'Disabling WiFi ...'
        echo_mock.assert_called_once_with(intro_msg)
        get_status_mock.assert_called_once()
        wifi_mock.assert_called_once()

    @patch.object(WiFi, '_disable_wifi')
    @patch.object(WiFi, '_get_wifi_status_code', return_value=0)
    @patch('click.echo')
    def test_turn_off_wifi_error(self, echo_mock, get_status_mock, wifi_mock):
        """
            Assert click.echo was called with the correct message passed
            as the argument.
            Assert WiFi._get_wifi_status_code was called and that if
            it returns 0 (disabled), click.echo is called with the correct
            error message.
        """
        self.wifi.turn_off()
        expected_err_msg = call('WiFi is already disabled. Skipping.')
        get_status_mock.assert_called_once()
        echo_mock.assert_has_calls([expected_err_msg])

    @patch.object(WiFi, '_get_wifi_status_code', return_value=1)
    @patch.object(WiFi, 'translate_status_code', return_value=colored("enabled", "green"))
    @patch('click.echo')
    def test_print_wifi_status(self, echo_mock, translate_mock, get_status_mock):
        """
            Assert Wifi.print_status() correctly retrieves the current
            wireless state, translates it to a colored string and outputs
            the correct message to the user.
        """
        expected_output = f'WiFi is {colored("enabled", "green")}'
        wifi_prop = DBUS_GENERAL_PROPS[self.wifi.wifi_prop]

        self.wifi.print_status()

        get_status_mock.assert_called_once()
        translate_mock.assert_called_once_with(wifi_prop, 1)
        echo_mock.assert_called_once_with(expected_output)

    @patch.object(WiFi, 'set_object_property')
    def test_enable_wifi(self, set_prop_mock):
        """
            Assert Wifi._enable_wifi() calls its inherited
            set_object_property method passing it the correct
            proxy, prop name and value (True in this case).
        """

        self.wifi._enable_wifi()
        set_prop_mock.assert_called_once_with(
            proxy=self.wifi.proxy,
            prop_name=self.wifi.wifi_prop,
            value=True
        )

    @patch.object(WiFi, 'set_object_property')
    def test_disable_wifi(self, set_prop_mock):
        """
            Assert Wifi._disable_wifi() calls its inherited
            set_object_property method passing it the correct
            proxy, prop name and value (False in this case).
        """

        self.wifi._disable_wifi()
        set_prop_mock.assert_called_once_with(
            proxy=self.wifi.proxy,
            prop_name=self.wifi.wifi_prop,
            value=False
        )

    @patch.object(WiFi, 'get_object_property')
    def test_get_wifi_status_code(self, get_prop_mock):
        self.wifi._get_wifi_status_code()
        get_prop_mock.assert_called_once_with(
            proxy=self.wifi.proxy,
            prop_name=self.wifi.wifi_prop
        )