import click
from wypy.wypy import WyPy
from termcolor import colored


class General(WyPy):

    def __init__(self, bus_name, obj_path, iface):
        super().__init__(bus_name, obj_path, iface)
        self.status_properties = [
            'State', 'Connectivity', 'WirelessEnabled',
            'WirelessHardwareEnabled', 'WwanEnabled',
            'WwanHardwareEnabled'
        ]
        self.property_names = [
            'STATE', 'CONNECTIVITY',
            'WIFI', 'WIFI-HW', 'WWAN',
            'WWAN-HW'
        ]

    def show_status(self):
        status_info = self._get_status_info()
        click.echo('WyPy - General status report \n')
        for name, status in zip(self.property_names, status_info):
            print(f'{name}: {self._translate_status_code(name, status)} \n')

    def get_hostname(self):
        print('running wypy general hostname from class')

    def _get_status_info(self):
        status = [
            str(self.get_object_property(prop))
            for prop in self.status_properties
        ]
        return status

    def _translate_status_code(self, prop, code):
        code = int(code)

        if prop == 'CONNECTIVITY':

            if code == 0:
                return colored('unknown', 'red')

            if code == 1:
                return colored('none', 'red')

            if code == 2:
                return colored('portal', 'yellow')

            if code == 3:
                return colored('limited', 'green')

            if code == 4:
                return colored('full', 'green')

        if prop == 'STATE':
            if code == 0:
                return colored('unknown', 'red')

            if code == 10:
                return colored('asleep', 'yellow')

            if code == 20:
                return colored('disconnected', 'red')

            if code == 30:
                return colored('disconnecting', 'red')

            if code == 40:
                return colored('connecting', 'yellow')

            if code == 50:
                return colored('connected (local)', 'green')

            if code == 60:
                return colored('connected (site)', 'green')

            if code == 70:
                return colored('connected', 'green')

        if prop in ['WIFI', 'WIFI-HW', 'WWAN', 'WWAN-HW']:
            if code == 1:
                return colored('enabled', 'green')
            if code == 0:
                return colored('diabled', 'red')
