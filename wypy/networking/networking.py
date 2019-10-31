import click
from wypy.wypy import WyPy
from wypy.utils.constants import NM_IFACE, NM_OBJ_PATH, NM_DEVICE_IFACE


class Network(WyPy):

    def __init__(self, obj_path=None):
        super().__init__(obj_path)

    def get_connectivity_state(self):
        """
        Get the general connectivity information
        """
        props = self.get_object_property('Connectivity')
        click.echo(f'Connectivity State: {props["Connectivity"]}')

    def turn_on(self):
        pass

    def turn_off(self):
        pass

    def check_connectivity(self):
        pass

    def _get_all_devices(self):
        pass