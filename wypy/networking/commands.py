import click
from .networking import Network


@click.group('network')
@click.pass_context
def network(ctx):
    """Perform networking actions"""
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
@click.option(
    '--check',
    is_flag=True,
    help='force WyPy to recheck connectivity state'
)
@click.pass_obj
def connectivity(network, check):
    """
    Get connectivity state.
    If check is passed, WyPy will perform a check on NetworkManager
    """
    if check:
        network.check_connectivity()
    else:
        network.get_connectivity_state()


network.add_command(turn_on)
network.add_command(turn_off)
network.add_command(connectivity)
