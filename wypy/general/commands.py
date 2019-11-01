import click
from .general import General


@click.group('general')
def general():
    pass


@general.command()
def status():
    """Print general NetworkManager status"""
    gen = General()
    gen.show_status()


@general.command()
def hostname():
    """Print hostname"""
    gen = General()
    gen.get_hostname()


general.add_command(status)
general.add_command(hostname)
