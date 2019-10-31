import dbus
from wypy.utils.constants import NM_BUS_NAME


class WyPy(object):

    def __init__(self, obj_path, bus_name=NM_BUS_NAME):
        self.bus = dbus.SystemBus()
        self.bus_name = bus_name
        self.obj_path = obj_path
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
   
    def get_all_properties(self, object_path, iface_name):
        proxy = self.bus.get_object(self.bus_name, object_path)
        iface = dbus.Interface(proxy, dbus.PROPERTIES_IFACE)
        return iface.GetAll(iface_name)
