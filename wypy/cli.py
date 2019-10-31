import click
from wypy.general.commands import general as general_commands
from wypy.networking.commands import network as network_commands
from wypy.utils.constants import VERSION


@click.group()
@click.version_option(version=VERSION, message=f'WyPy - Version {VERSION}')
def cli():
    """
    wypy is command line NetworkManager utility.
    """
    pass


cli.add_command(general_commands)
cli.add_command(network_commands)

if __name__ == "__main__":
    cli()
