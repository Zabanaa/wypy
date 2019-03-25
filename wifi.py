import dbus
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib

DBusGMainLoop(set_as_default=True)

loop = GLib.MainLoop()

bus = dbus.SystemBus()
proxy_object = bus.get_object(
    'org.freedesktop.NetworkManager',
    '/org/freedesktop/NetworkManager'
)

# Define our signal handler callback.
# Network Manager states:
#
# NM_STATE_DISCONNECTED     -> 20
# NM_STATE_DISCONNECTING    -> 30
# NM_STATE_CONNECTING       -> 40
# NM_STATE_CONNECTED_LOCAL  -> 50
# NM_STATE_CONNECTED_SITE   -> 60
# NM_STATE_CONNECTED_GLOBAL -> 70


def network_state_change_handler(new_state):
    print(new_state)


bus.add_signal_receiver(
    network_state_change_handler,
    signal_name='StateChanged',
    dbus_interface='org.freedesktop.NetworkManager'
)

loop.run()
