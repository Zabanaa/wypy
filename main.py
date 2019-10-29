import dbus

NM_BUS_NAME = 'org.freedesktop.NetworkManager'
NM_IFACE = 'org.freedesktop.NetworkManager'
NM_BUS_OBJ = '/org/freedesktop/NetworkManager'

## Connect to the system bus
bus = dbus.SystemBus()

## get the network manager object (proxy)
nm = bus.get_object(NM_BUS_NAME, NM_BUS_OBJ)

devices = nm.Get(NM_BUS_NAME, 'AllDevices', dbus_interface=dbus.PROPERTIES_IFACE)

for device in devices:
    dev = bus.get_object(NM_BUS_NAME, device)
    dev_name = dev.Get(NM_BUS_NAME + '.Device', 'Interface', dbus_interface=dbus.PROPERTIES_IFACE)
    print(dev_name)
