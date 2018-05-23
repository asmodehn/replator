import os
import palimport
from lark import Lark, InlineTransformer


if __package__:
    from .parse import bfck
else:
    from parse import bfck


# For some kind of safe interface
import io


class BrainfuckPython(InlineTransformer):

    # TODO : AST https://docs.python.org/3/library/ast.html#module-ast
    def __init__(self):
        self.indent = ""

    def start(self, *args):
        return """
arr = bytearray(30000)
ptr = 0
{instr}
""".format(instr="\n".join(args))

    def incr(self):
        return """
{0}arr[ptr] += 1""".format(self.indent)

    def decr(self):
        return """
{0}arr[ptr] -= 1""".format(self.indent)

    def ptri(self):
        return """
{0}ptr++""".format(self.indent)

    def ptrd(self):
        return """
{0}ptr--""".format(self.indent)

    def loop(self,*args):
        self.indent += "  "
        yield """
{0}while (arr[ptr]):""".format(self.indent)
        self.indent -= "  "

    def outp(self):
        return """
{0}write(arr[ptr])""".format(self.indent)

    def inpt(self):
        return """
{0}arr[ptr]=read(1)""".format(self.indent)


class BfckLoader(palimport.Loader):
    """
    Custom Loader, loading a custom AST into python code.
    """
    parser = bfck.parser
    transformer = BrainfuckPython()


def interp(s):
    AST = bfck.parser.parse(s)
    pysource = BrainfuckPython().transform(AST)
    # TODO : fix that in the grammar
    if not isinstance(pysource, (str,)):
        pysource = str(pysource)
    return pysource


# to be able to test basic interpreting functionality
if __name__ == '__main__':
    outstream = io.BytesIO()
    instream = io.BytesIO()
    gbls = {'__builtins__': {'bytearray': bytearray}, 'write': lambda b: outstream.write(bytes(b)), 'read': instream.read}
    lcls = {}
    while True:
        try:
            s = input('bfck> ')
        except EOFError:
            break
        # Ref : http://lucumr.pocoo.org/2011/2/1/exec-in-python/
        pysource = interp(s)
        print(pysource)
        pycode = compile(pysource, '<string>', 'exec')
        # TODO : AST | dis: decompile
        exec(pycode, gbls, lcls)
        print(str(outstream.getvalue()))

# cheatsheet

# 3 + 5 :
#
# +++       store 3 in #0
# >         move to #1
# +++++     store 5 in #1
# [-<+>]    loop: dec #1 inc #0
# <         move to #0

# 4 * 7
#
# >++++      store 4 in  #1
# [-         loop: dec #1
# <               move to #0
# +++++++         inc 7 times #0
# >               move to #1
# ]
# <          move to #0

# 2^10
#
# +              store 1 in #0
# >>++++++++++   store 10 in #2
# [ <<           loop:
# [>++<-]        #1 contains the double of #0
# >              move to #1
# [<+>-]         move the value from #1 to #0
# >-             dec #3
# ]
# <<             move to #0



# +++>+++++[-<+>].<
