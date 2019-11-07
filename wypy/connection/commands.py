import click
from .connection import Connection


@click.group('connection')
@click.pass_context
def connection(ctx):
    ctx.obj = Connection()


@click.command('down')
@click.argument('id', type=str, required=True)
@click.pass_obj
def down(conn, name):
    """Deactivate a connection"""
    conn.deactivate(name)


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


@click.command('delete')
@click.argument('name', type=str, required=True)
@click.pass_obj
def delete(conn, name):
    """Delete a connection profile"""
    conn.delete(name)


connection.add_command(down)
connection.add_command(_list)
connection.add_command(list_active)
connection.add_command(delete)
