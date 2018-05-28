import os
import sys
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import Completer, Completion
import click
from fuzzyfinder import fuzzyfinder
from pygments.lexers.sql import SqlLexer

import click
from click_repl import register_repl

"""
A Terminal interface to your OS.
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



import click
from click_repl import repl as crepl
from prompt_toolkit.history import FileHistory


from replator.calc.interp import interp

# CalcKeywords = ['select', 'from', 'insert', 'update', 'delete', 'drop']

# class SQLCompleter(Completer):
#     def get_completions(self, document, complete_event):
#         word_before_cursor = document.get_word_before_cursor(WORD=True)
#         matches = fuzzyfinder(word_before_cursor, SQLKeywords)
#         for m in matches:
#             yield Completion(m, start_position=-len(word_before_cursor))


lcls = {}

replator_path = os.path.join(os.path.expanduser('~'), '.replator')

@click.group()
def cli():
    if not os.path.exists(replator_path):
        os.mkdir(replator_path)

    pass


@cli.command()
def repl():
    """
    repl for shell commands.
    """
    prompt_kwargs = {
        'message': u'repl> ',
        'history': FileHistory(os.path.join(replator_path,'repl-history.txt')),
        'auto_suggest': AutoSuggestFromHistory()
    }

    crepl(click.get_current_context(), prompt_kwargs=prompt_kwargs)


@cli.command()
def calc():
    """
    calc repl
    """
    global lcls

    while True:
        try:
            user_input = prompt(message=u'calc>',
                                history=FileHistory(os.path.join(replator_path, 'calc-history.txt')),
                                auto_suggest=AutoSuggestFromHistory(),
                                #                        completer=SQLCompleter(),
                                #                        lexer=SqlLexer,
                                )
        except KeyboardInterrupt:
            continue
        except EOFError:
            break

        # Ref : http://lucumr.pocoo.org/2011/2/1/exec-in-python/
        pysource = interp(user_input)
        pycode = compile(pysource, '<string>', 'single')
        exec(pycode, {"__builtins__": None}, lcls)

        #click.echo_via_pager(user_input)


if '__main__' == __name__:
    cli()
