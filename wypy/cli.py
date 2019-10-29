import click
from wypy.general.commands import general as general_commands


@click.group()
def cli():
    """
    wypy is command line NetworkManager utility.
    """
    pass


cli.add_command(general_commands)

if __name__ == "__main__":
    cli()
