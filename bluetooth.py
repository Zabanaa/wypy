import dbus
import dbus.glib
import gtk

bus = dbus.SystemBus()

manager_object = bus.get_object('org.bluez', '/org/bluez')
manager = dbus.Interface(manager_object, 'org.bluez.ProfileManager')

adapter = dbus.Interface(
    bus.get_object('org.bluez', manager.get_dbus_method('DefaultAdapter')),
    'org.bluez.Adapter1')



# def remote_device_found(addr, class_, rssi):
#     print("Addr ", addr)
#     print("Rssi ", rssi)


# def discovery_completed():
#     gtk.main_quit()


# adapter.connect_to_signal('RemoteDeviceFound', remote_device_found)
# adapter.connect_to_signal('DiscoveryCompleted', discovery_completed)

# adapter.DiscoverDevices()
# gtk.main()
