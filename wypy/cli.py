import click


@click.group()
def cli():
    """
    wypy is command line NetworkManager utility.
    """
    pass

@click.command()
def hello():
    """Print hello to the screen"""
    click.echo('Hello World')


cli.add_command(hello)

if __name__ == "__main__":
    cli()