import click
from package.worker import main
from package.auto import auto_scan

@click.group()
def cli():
    click.echo('Infoc')

@click.command()
@click.argument('input_list', type=click.Path(exists=True))
def nmap(input_list):
    click.echo(input_list)
    main(input_list)

@click.command()
@click.argument('input_list', type=click.Path(exists=True))
def scnr(input_list):
    click.echo(input_list)
    auto_scan(input_list)

cli.add_command(nmap)
cli.add_command(scnr)