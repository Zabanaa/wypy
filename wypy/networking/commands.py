import click


@click.group('network')
def network():
    pass


@click.command('on')
def turn_on():
    """Turn networking capabiliy on"""
    click.echo('turn networking on')


@click.command('off')
def turn_off():
    """Turn networking capabiliy off"""
    click.echo('set all managed devices to unmanaged')


@click.command('connectivity')
@click.option('--check', is_flag=True)
def connectivity(check):
    if check:
        click.echo('Checking connectivity again ...')
    """
    Get connectivity state.
    If check is passed, WyPy will perform a check on NetworkManager
    """
    click.echo('check connectivity heheh')


network.add_command(turn_on)
network.add_command(turn_off)
network.add_command(connectivity)
