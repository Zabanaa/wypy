import dbus

NM_BUS_NAME = 'org.freedesktop.NetworkManager'
NM_IFACE = 'org.freedesktop.NetworkManager'
NM_BUS_OBJ = '/org/freedesktop/NetworkManager/Settings'

# Connect to the system bus
bus = dbus.SystemBus()

# get the network manager object (proxy)

# props = [
#     'State', 'WirelessEnabled',
#     'WirelessHardwareEnabled', 'WwanEnabled',
#     'WwanHardwareEnabled'
# ]

# nm = bus.get_object(NM_BUS_NAME, NM_BUS_OBJ)

# host = nm.Get(
#     NM_BUS_NAME + '.Settings',
#     'Hostname',
#     dbus_interface=dbus.PROPERTIES_IFACE
# )

# print(host)

proxy = bus.get_object(NM_BUS_NAME, '/' + NM_IFACE.replace('.', '/'))
nm = dbus.Interface(proxy, NM_IFACE)
devices = nm.GetDevices()

for device in devices:
    print(device)
    proxy = bus.get_object(NM_BUS_NAME, device)
    dev_iface = dbus.Interface(proxy, dbus.PROPERTIES_IFACE)
    device_props = dev_iface.GetAll('org.freedesktop.NetworkManager.Device')
    print(device_props['Udi'], device_props['Interface'])
