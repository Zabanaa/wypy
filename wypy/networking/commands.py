import click
from .networking import Network


@click.group('network')
def network():
    pass


@click.command('on')
def turn_on():
    """Turn networking capabiliy on"""
    click.echo('Enabling networking capability')
    network = Network()
    network.turn_on()


@click.command('off')
def turn_off():
    """Turn networking capabiliy off"""
    click.echo('Disabling networking capability')
    network = Network()
    network = network.turn_off()


@click.command('connectivity')
@click.option('--check', is_flag=True)
def connectivity(check):
    if check:
        click.echo('Checking connectivity again ...')
    """
    Get connectivity state.
    If check is passed, WyPy will perform a check on NetworkManager
    """
    network = Network()
    network.get_connectivity_state()


network.add_command(turn_on)
network.add_command(turn_off)
network.add_command(connectivity)
