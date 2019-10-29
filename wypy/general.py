import click


class General(object):

    @classmethod
    def status():
        click.echo('wypy general status command')

    @classmethod
    def get_hostname():
        click.echo('wypy general hostname')
