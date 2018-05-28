import os
import palimport
from lark import Lark, InlineTransformer


if __package__:
    from .parse import calc
else:
    from parse import calc


class CalculatePython(InlineTransformer):
    from operator import add, sub, mul, truediv as div, neg
    number = float

    def __init__(self):
        pass

    # TODO : AST https://docs.python.org/3/library/ast.html#module-ast
    def assign_var(self, name, value):
        # translate to python code instead of direct evaluation
        return "{name} = {value}".format(**locals())

    def var(self, name):
        # translate to python code instead of direct evaluation
        return "{name}".format(**locals())

    def exit(self):
        "calling exit method of the current repl"
        return "exit()"


class CalcLoader(palimport.Loader):
    """
    Custom Loader, loading a custom AST into python code.
    """
    parser = calc.parser
    transformer = CalculatePython()


def interp(s):
    AST = calc.parser.parse(s)
    pysource = CalculatePython().transform(AST)
    # TODO : fix that in the grammar
    if not isinstance(pysource, (str,)):
        pysource = str(pysource)
    return pysource


# to be able to test basic interpreting functionality
if __name__ == '__main__':
    lcls = {}
    while True:
        try:
            s = input('calc> ')
        except KeyboardInterrupt:
            continue
        except EOFError:
            break
        # Ref : http://lucumr.pocoo.org/2011/2/1/exec-in-python/
        pysource = interp(s)
        pycode = compile(pysource, '<string>', 'single')
        exec(pycode, {"__builtins__": None}, lcls)

