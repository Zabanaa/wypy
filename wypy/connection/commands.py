import click
from .connection import Connection


@click.group('connection')
@click.pass_context
def connection(ctx):
    ctx.obj = Connection()


@click.command('up')
@click.pass_obj
def up(conn):
    """Activate a connection"""
    conn.activate()


@click.command('down')
@click.pass_obj
def down(conn):
    """Deactivate a connection"""
    conn.deactivate()


@click.command('show')
@click.option('--active', is_flag=True)
@click.pass_obj
def show(conn, active):
    """List connections"""
    if not active:
        conn.show_all()
    else:
        conn.show_active()


connection.add_command(up)
connection.add_command(down)
connection.add_command(show)
