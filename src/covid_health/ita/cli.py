import click
from .prep_istat import cli as istat
from .prep_salutegov import cli as salutegov
from .prep_other_data import cli as other_data


@click.group(help="Datasets creation from Italian Data Sources.")
def cli():
    pass

cli.add_command(istat, name='istat')
cli.add_command(salutegov, name='salute-gov')
cli.add_command(other_data, name='metadata')


def main():
    cli()


if __name__ == "__main__":
    main()
