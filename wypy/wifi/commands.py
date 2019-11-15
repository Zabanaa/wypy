from .wifi import WiFi
import click


@click.group('wifi')
@click.pass_context
def wifi(ctx):
    """Interact with the wireless device(s)"""
    ctx.obj = WiFi()


@click.command('on')
@click.pass_obj
def turn_wifi_on(wifi):
    """Enable WiFi"""
    wifi.turn_on()


@click.command('off')
@click.pass_obj
def turn_wifi_off(wifi):
    """Disable WiFi"""
    wifi.turn_off()


@click.command('status')
@click.pass_obj
def wifi_status(wifi):
    """Print current WiFi status"""
    wifi.print_status()


@click.command('list')
@click.pass_obj
def list_access_points(wifi):
    """List currently available access points"""
    wifi.list_access_points()


@click.command('rescan')
@click.pass_obj
def rescan(wifi):
    """Force WyPy to scan for available access points"""
    wifi.rescan()


@click.command('connect')
@click.pass_obj
def connect(wifi):
    """Connect to a wireless access point"""
    wifi.connect()


wifi.add_command(turn_wifi_on)
wifi.add_command(turn_wifi_off)
wifi.add_command(wifi_status)
wifi.add_command(list_access_points)
wifi.add_command(rescan)
wifi.add_command(connect)
