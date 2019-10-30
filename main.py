import dbus

NM_BUS_NAME = 'org.freedesktop.NetworkManager'
NM_IFACE = 'org.freedesktop.NetworkManager'
NM_BUS_OBJ = '/org/freedesktop/NetworkManager/Settings'

# Connect to the system bus
bus = dbus.SystemBus()

# get the network manager object (proxy)

props = [
    'State', 'WirelessEnabled',
    'WirelessHardwareEnabled', 'WwanEnabled',
    'WwanHardwareEnabled'
]

nm = bus.get_object(NM_BUS_NAME, NM_BUS_OBJ)

host = nm.Get(
    NM_BUS_NAME + '.Settings',
    'Hostname',
    dbus_interface=dbus.PROPERTIES_IFACE
)

print(host)
# devices = nm.Get(
#     NM_BUS_NAME,
#     'WirelessEnabled',
#     dbus_interface=dbus.PROPERTIES_IFACE
# )

# print(devices)

# for device in devices:
#     dev = bus.get_object(NM_BUS_NAME, device)
#     dev_name = dev.Get(
#         NM_BUS_NAME + '.Device',
#         'Interface',
#         dbus_interface=dbus.PROPERTIES_IFACE
#     )
#     print(dev_name)
