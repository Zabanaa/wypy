import dbus
from wypy.utils.constants import NM_BUS_NAME
from termcolor import colored


class WyPy(object):

    def __init__(self):
        self.bus = dbus.SystemBus()
        self.bus_name = NM_BUS_NAME

    def set_object_property(
        self,
        proxy=None,
        bus_name=None,
        prop_name=None,
        value=None,
        iface=dbus.PROPERTIES_IFACE
    ):
        _bus_name = bus_name if bus_name else self.bus_name
        return proxy.Set(
            _bus_name,
            prop_name,
            value,
            dbus_interface=iface
        )

    def get_object_property(
        self,
        proxy=None,
        bus_name=None,
        prop_name=None,
        iface=dbus.PROPERTIES_IFACE
    ):
        _bus_name = bus_name if bus_name else self.bus_name
        return proxy.Get(
            _bus_name,
            prop_name,
            dbus_interface=iface
        )

    def get_all_properties(self, object_path, iface_name):
        proxy = self.bus.get_object(self.bus_name, object_path)
        iface = dbus.Interface(proxy, dbus.PROPERTIES_IFACE)
        return iface.GetAll(iface_name)

    def translate_status_code(self, prop, code):

        if prop == 'CONNECTIVITY':

            if code == 0:
                return colored('unknown', 'red')

            if code == 1:
                return colored('none', 'red')

            if code == 2:
                return colored('portal', 'yellow')

            if code == 3:
                return colored('limited', 'green')

            if code == 4:
                return colored('full', 'green')

        if prop == 'STATE':
            if code == 0:
                return colored('unknown', 'red')

            if code == 10:
                return colored('asleep', 'yellow')

            if code == 20:
                return colored('disconnected', 'red')

            if code == 30:
                return colored('disconnecting', 'red')

            if code == 40:
                return colored('connecting', 'yellow')

            if code == 50:
                return colored('connected (local)', 'green')

            if code == 60:
                return colored('connected (site)', 'green')

            if code == 70:
                return colored('connected', 'green')

        if prop in ['NETWORKING', 'WIFI', 'WIFI-HW', 'WWAN', 'WWAN-HW']:
            if code == 1:
                return colored('enabled', 'green')
            if code == 0:
                return colored('disabled', 'red')

    def translate_device_type(self, _type):
        if _type == 30:
            return 'WiFi P2P'

        if _type == 29:
            return 'WireGuard'

        if _type == 28:
            return '6LoWPAN'

        if _type == 27:
            return 'WPAN'

        if _type == 26:
            return 'Open vSwitch Bridge'

        if _type == 25:
            return 'Openv Switch Port'

        if _type == 24:
            return 'Openv Switch Interface'

        if _type == 23:
            return 'PPP'

        if _type == 22:
            return 'Dummy'

        if _type == 21:
            return 'MACsec'

        if _type == 20:
            return 'VETH'

        if _type == 19:
            return 'VXLAN'

        if _type == 18:
            return 'MACVLAN'

        if _type == 17:
            return 'IP tunnel'

        if _type == 16:
            return 'TUN/TAP'

        if _type == 15:
            return 'Team Master'

        if _type == 14:
            return 'Generic / Loopback'

        if _type == 13:
            return 'Bridge'

        if _type == 12:
            return 'ADSL Modem'

        if _type == 11:
            return 'VLAN'

        if _type == 10:
            return 'Bond'

        if _type == 9:
            return 'IP Infiniband'

        if _type == 8:
            return 'Modem'

        if _type == 7:
            return 'WiMax'

        if _type == 6:
            return 'OLPC XO Mesh'

        if _type == 5:
            return 'Bluetooth'

        if _type in [4, 3]:
            return 'Unused'

        if _type == 2:
            return 'WiFi'

        if _type == 1:
            return 'Ethernet'

        if _type == 0:
            return 'Unknown'

    def translate_device_state(self, status):
        if status == 120:
            return 'failed'
        if status == 110:
            return 'deactivating'
        if status == 100:
            return "connected"
        if status == 90:
            return "secondaries"
        if status == 80:
            return "ip check"
        if status == 70:
            return "ip config"
        if status == 60:
            return "auth required"
        if status == 50:
            return "configuring"
        if status == 40:
            return "preparing"
        if status == 30:
            return "disconnected"
        if status == 20:
            return "unavailable"
        if status == 10:
            return "unmanaged"

    def get_device_state_row_color(self, status):
        if status == 100:
            return "green"
        elif status in [120, 110, 30]:
            return "red"
        else:
            return "yellow"
