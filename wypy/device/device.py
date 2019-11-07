from wypy.wypy import WyPy
import click


class Device(WyPy):

    def __init__(self):
        super().__init__()

    def print_status(self):
        click.echo('Showing status ...')

    def list_all(self):
        click.echo('list all devices ...')

    def print_details(self, device_name):
        click.echo(f'Showing device details for {device_name}...')
