import click
from .general import General


@click.group('general')
@click.pass_context
def general(ctx):
    ctx.obj = General()


@click.command()
@click.pass_obj
def status(gen):
    """Print general NetworkManager status"""
    gen.show_status()


@general.command()
@click.pass_obj
def hostname(gen):
    """Print hostname"""
    gen.get_hostname()


general.add_command(status)
general.add_command(hostname)
