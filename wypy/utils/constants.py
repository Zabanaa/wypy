VERSION = '0.1.0'
NM_BUS_NAME = 'org.freedesktop.NetworkManager'

NM_OBJ_PATH = '/org/freedesktop/NetworkManager'

NM_SETTINGS_OBJ_PATH = '/org/freedesktop/NetworkManager/Settings'
NM_SETTINGS_IFACE = 'org.freedesktop.NetworkManager.Settings'

NM_IFACE = 'org.freedesktop.NetworkManager'

NM_DEVICE_IFACE = 'org.freedesktop.NetworkManager.Device'

NM_ACTIVE_CONN_IFACE = 'org.freedesktop.NetworkManager.Connection.Active'

NM_CONNECTION_IFACE = 'org.freedesktop.NetworkManager.Settings.Connection'

IP4_CONFIG_IFACE = 'org.freedesktop.NetworkManager.IP4Config'

NM_WIRELESS_IFACE = 'org.freedesktop.NetworkManager.Device.Wireless'

NM_ACCESS_POINT_IFACE = 'org.freedesktop.NetworkManager.AccessPoint'

NM_CONNECTION_STATE_ACTIVATED = 2

DBUS_GENERAL_PROPS = {
    'Connectivity': 'CONNECTIVITY',
    'State': 'STATE',
    'WirelessEnabled': 'WIFI',
    'WwanEnabled': 'WWAN',
    'WirelessHardwareEnabled': 'WIFI-HW',
    'WwanHardwareEnabled': 'WWAN-HW'
}
