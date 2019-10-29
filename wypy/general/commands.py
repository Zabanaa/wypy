import click
from .general import General


@click.group('general')
def general():
    pass


@general.command()
def status():
    General.status()


@general.command()
def hostname():
    General.get_hostname()


general.add_command(status)
general.add_command(hostname)
