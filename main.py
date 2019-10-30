import dbus

NM_BUS_NAME = 'org.freedesktop.NetworkManager'
NM_IFACE = 'org.freedesktop.NetworkManager'
NM_BUS_OBJ = '/org/freedesktop/NetworkManager'

# Connect to the system bus
bus = dbus.SystemBus()

# get the network manager object (proxy)

props = [
    'State', 'WirelessEnabled',
    'WirelessHardwareEnabled', 'WwanEnabled',
    'WwanHardwareEnabled'
]

nm = bus.get_object(NM_BUS_NAME, NM_BUS_OBJ)


def get_dbus_object_property(prop_name):
    # maybe there should be a try/except

    return nm.Get(
        NM_BUS_NAME,
        prop_name,
        dbus_interface=dbus.PROPERTIES_IFACE
    )


state = [get_dbus_object_property(prop) for prop in props]
# state = nm.state(dbus_interface=NM_IFACE)
for prop in state:
    print(prop)

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
