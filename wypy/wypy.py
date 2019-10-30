import dbus


class WyPy(object):

    def __init__(self, bus_name, obj_path, iface):
        self.bus = dbus.SystemBus()
        self.bus_name = bus_name
        self.obj_path = obj_path
        self.iface = iface
        self.proxy = self.bus.get_object(self.bus_name, self.obj_path)

    def get_object_property(
        self,
        prop_name,
        iface=dbus.PROPERTIES_IFACE
    ):
        return self.proxy.Get(
            self.bus_name,
            prop_name,
            dbus_interface=iface
        )
