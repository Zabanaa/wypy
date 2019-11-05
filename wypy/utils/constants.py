VERSION = '0.1.0'
NM_BUS_NAME = 'org.freedesktop.NetworkManager'

NM_OBJ_PATH = '/org/freedesktop/NetworkManager'

NM_SETTINGS_OBJ_PATH = '/org/freedesktop/NetworkManager/Settings'
NM_SETTINGS_IFACE = 'org.freedesktop.NetworkManager.Settings'

NM_IFACE = 'org.freedesktop.NetworkManager'

NM_DEVICE_IFACE = 'org.freedesktop.NetworkManager.Device'

NM_ACTIVE_CONN_IFACE = 'org.freedesktop.NetworkManager.Connection.Active'

DBUS_GENERAL_PROPS = {
    'Connectivity': 'CONNECTIVITY',
    'State': 'STATE',
    'WirelessEnabled': 'WIFI',
    'WwanEnabled': 'WWAN',
    'WirelessHardwareEnabled': 'WIFI-HW',
    'WwanHardwareEnabled': 'WWAN-HW'
}