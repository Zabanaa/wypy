import click
from .device import Device


@click.group('device')
@click.pass_context
def device(ctx):
    ctx.obj = Device()


@click.command('status')
@click.pass_obj
def status(dev):
    """Print general device status information"""
    dev.print_status()


@click.command('list')
@click.pass_obj
def list_all(dev):
    """List detailed device information"""
    dev.list_all()


@click.command('get')
@click.argument('name', type=str, required=True)
@click.pass_obj
def get(dev, name):
    """List detailed device information for a given device"""
    dev.print_details(name)


device.add_command(status)
device.add_command(list_all)
device.add_command(get)
