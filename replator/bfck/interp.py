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

    def start(self, *args):
        return """ptr = 0\n{instr}\n""".format(instr="\n".join(args))

    def incr(self):
        return """arr[ptr] += 1"""

    def decr(self):
        return """arr[ptr] -= 1"""

    def ptri(self):
        return """ptr += 1"""

    def ptrd(self):
        return """ptr -= 1"""

    def loop(self, *args):
        # managing indentation in a way compatible with the grammar and parser.
        args = ["  "+sl for a in args for sl in a.splitlines()]
        return """while (arr[ptr]):\n{instr}\n""".format(instr="\n".join(args))

    def outp(self):
        return """write(arr[ptr:ptr+1])"""

    def inpt(self):
        return """arr[ptr]=read(1)"""


class BfckLoader(palimport.Loader):
    """
    Custom Loader, loading a custom AST into python code.
    """
    parser = bfck.parser
    transformer = BrainfuckPython()


class BfckREPL(object):
    """
    class storing all information for this REPL
    It is usable as a context manager.
    """

    def __init__(self, transformer, arr_size=30000):
        self.transformer = transformer
        self.arr_size = arr_size
        self.arr = bytearray(self.arr_size)
        self.outstream = io.BytesIO()
        self.instream = io.BytesIO()
        self.gbls = {'__builtins__': {'arr': self.arr},
                'write': lambda b: self.outstream.write(b),
                'read': self.instream.read}

    def __enter__(self):
        """entering REPL"""
        self.indent = ""
        self.ptr = 0
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __call__(self,):
        locals = {}
        while True:
            print(">>> " + str(self.outstream.getvalue()))
            s = input('bfck> ')
            # Ref : http://lucumr.pocoo.org/2011/2/1/exec-in-python/
            AST = bfck.parser.parse(s)
            pysource = self.transformer.transform(AST)
            # TODO : fix that in the grammar
            if not isinstance(pysource, (str,)):
                pysource = str(pysource)
            print("<<< " + "\n<<< ".join(pysource.split("\n")))
            pycode = compile(pysource, '<string>', 'exec')
            # TODO : AST | dis: decompile
            exec(pycode, self.gbls, locals)


if __name__ == '__main__':
    with BfckREPL(BrainfuckPython()) as repl:
        try:
            repl()
        except KeyboardInterrupt:
            raise
        except EOFError:
            raise

        # auto cleanup and reload ? ( how about tower of interpreters ? )



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



# +++>+++++[-<+>].<.
# [ [ + ] - ] .
# [[+]-].