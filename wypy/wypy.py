import dbus
from wypy.utils.constants import NM_BUS_NAME
from termcolor import colored


class WyPy(object):

    def __init__(self, bus_name=NM_BUS_NAME):
        self.bus = dbus.SystemBus()
        self.bus_name = bus_name

    def get_object_property(
        self,
        proxy,
        prop_name,
        iface=dbus.PROPERTIES_IFACE
    ):
        return proxy.Get(
            self.bus_name,
            prop_name,
            dbus_interface=iface
        )

    def get_all_properties(self, object_path, iface_name):
        proxy = self.bus.get_object(self.bus_name, object_path)
        iface = dbus.Interface(proxy, dbus.PROPERTIES_IFACE)
        return iface.GetAll(iface_name)

    def _translate_status_code(self, prop, code):

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

        if prop in ['WIFI', 'WIFI-HW', 'WWAN', 'WWAN-HW']:
            if code == 1:
                return colored('enabled', 'green')
            if code == 0:
                return colored('disabled', 'red')