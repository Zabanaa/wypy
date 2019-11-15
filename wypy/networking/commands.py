import click
from .networking import Network


@click.group('network')
@click.pass_context
def network(ctx):
    ctx.obj = Network()


@click.command('on')
@click.pass_obj
def turn_on(network):
    """Turn networking capabiliy on"""
    network.turn_on()


@click.command('off')
@click.pass_obj
def turn_off(network):
    """Turn networking capabiliy off"""
    network = network.turn_off()


@click.command('connectivity')
@click.option('--check', is_flag=True)
@click.pass_obj
def connectivity(network, check):
    if check:
        click.echo('Checking connectivity again ...')
    """
    Get connectivity state.
    If check is passed, WyPy will perform a check on NetworkManager
    """
    network.get_connectivity_state()


network.add_command(turn_on)
network.add_command(turn_off)
network.add_command(connectivity)
