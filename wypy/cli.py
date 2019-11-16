import click
import sys
from termcolor import colored
from wypy.utils.helpers import nm_is_installed
from wypy.device.commands import device as device_commands
from wypy.general.commands import general as general_commands
from wypy.networking.commands import network as network_commands
from wypy.wifi.commands import wifi as wifi_commands
from wypy.connection.commands import connection as conn_commands
from wypy.utils.constants import VERSION


@click.group()
@click.version_option(version=VERSION, message=f'WyPy - Version {VERSION}')
def cli():
    """
    wypy is a command line utility for NetworkManager.
    """
    pass


cli.add_command(general_commands)
cli.add_command(network_commands)
cli.add_command(wifi_commands)
cli.add_command(conn_commands)
cli.add_command(device_commands)

if __name__ == "__main__":
    is_nm_installed = nm_is_installed()
    if is_nm_installed:
        cli()
    else:
        msg = """
        [Error]: NetworkManager must be installed on the system to use WyPy.
        """.replace('  ', '')
        sys.exit(colored(msg, "red"))
