import click
from .ita.cli import cli as ita
from .prep_eurostat import cli as eurostat
from .prep_worldometer import cli as worldometer


@click.group()
def cli():
    pass

cli.add_command(ita, name='ita')
cli.add_command(eurostat, name='eurostat')
cli.add_command(worldometer, name='worldometers')


def main():
    cli()


if __name__ == "__main__":
    main()
