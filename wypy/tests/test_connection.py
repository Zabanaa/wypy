
from unittest.mock import patch, call
from wypy.connection import Connection
from wypy.utils.constants import (
    NM_OBJ_PATH,
    NM_IFACE,
    NM_BUS_NAME,
    DBUS_GENERAL_PROPS
)
import subprocess
import dbus
import dbusmock


class TestConnection(dbusmock.DBusTestCase):

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
        self.conn = Connection()

    def tearDown(self):
        self.p_mock.terminate()
        self.p_mock.wait()
