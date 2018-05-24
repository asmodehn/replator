import sys

import replator.display

import click
from click_repl import register_repl

"""
A Terminal interface to your OS, specialized for stack-based languages.
"""

#
# @click.command()
# @click.argument('file')
# def cli(file):
#     try:
#         name = sys.argv[1]
#         assert open(name, "a")
#     except:
#         sys.stderr.write(__doc__)
#         return
#     replator.display.Display(name).main()


# @cli.command()
# def calc():
#     """
#     running the calc interpreter
#     """
#
#
#
# @cli.command()
# def bfck():
#     """
#     running the bfck interpreter
#     """



# def main():
#     try:
#         name = sys.argv[1]
#         assert open(name, "a")
#     except:
#         sys.stderr.write(__doc__)
#         return
#     replator.display.Display(name).main()

@click.group()
def cli():
    pass

@cli.command()
def hello():
    click.echo("Hello world!")

register_repl(cli)
