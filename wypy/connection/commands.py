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


@click.command('list')
@click.pass_obj
def _list(conn):
    """List connections"""
    conn.show_all()


@click.command('active')
@click.pass_obj
def list_active(conn):
    """List active connections"""
    conn.show_active()


connection.add_command(up)
connection.add_command(down)
connection.add_command(_list)
connection.add_command(list_active)
