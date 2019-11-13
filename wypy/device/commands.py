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


@click.command('update')
@click.argument('ifname', type=str, required=True)
@click.pass_obj
def update(dev, ifname):
    """
    Update device by applying the last changes done
    to its active connection
    """
    dev.update_ifname_connection(ifname)


@click.command('disconnect')
@click.argument('ifname', type=str, required=True)
@click.pass_obj
def disconnect(dev, ifname):
    """Disconnect the device"""
    dev.disconnect(ifname)


@click.command('delete')
@click.argument('ifname', type=str, required=True)
@click.pass_obj
def delete(dev, ifname):
    """Delete the device"""
    dev.delete_iface(ifname)


device.add_command(status)
device.add_command(list_all)
device.add_command(get)
device.add_command(update)
device.add_command(disconnect)
device.add_command(delete)
