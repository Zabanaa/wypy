import click


class General(object):

    @classmethod
    def status(cls):
        click.echo('running wypy general status from class')

    @classmethod
    def get_hostname(cls):
        click.echo('running wypy general hostname from class')
