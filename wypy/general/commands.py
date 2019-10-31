import click
from .general import General
from wypy.utils.constants import NM_BUS_NAME, NM_OBJ_PATH


@click.group('general')
def general():
    pass


@general.command()
def status():
    """Print general NetworkManager status"""
    gen = General(NM_OBJ_PATH)
    gen.show_status()


@general.command()
def hostname():
    """Print hostname"""
    gen = General(NM_OBJ_PATH)
    gen.get_hostname()


general.add_command(status)
general.add_command(hostname)
