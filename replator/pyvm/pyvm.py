import io
import sys
import argparse
import code
import traceback
from contextlib import redirect_stdout, redirect_stderr
from codeop import CommandCompiler, compile_command
from collections import namedtuple
import inspect

# Inspired by Python's code module
# With a somewhat different design :
# The interpretator class is a isolated instance
# and allows only one in/out stream connection to it.

Interpreted = namedtuple("Interpreted", ["out", "prompt", "unused"])

def interpretator(interpreter = code.InteractiveInterpreter(), filename="<input>", symbol="single"):
    try:
        sys.ps1
    except AttributeError:
        sys.ps1 = ">>> "
    try:
        sys.ps2
    except AttributeError:
        sys.ps2 = "... "

    cprt = 'Type "help", "copyright", "credits" or "license" for more information.'
    banner = "Python %s on %s\n%s\n(%s)\n" % (sys.version, sys.platform, cprt, inspect.currentframe().f_code.co_name)

    try:
        while 1:
            # TODO : redirect stdin, stdout, stderr as sonas we re out of current process
            try:
                if banner:
                    source = yield Interpreted(banner, sys.ps1, [])
                    banner = None
                else:# Case 3 is also the default case with empty source
                    source = yield Interpreted("", sys.ps1, [])

                code = interpreter.compile(source, filename, symbol)
                while code is None:
                    # Case 2 : need more lines !!
                    # TODO : return formatted source
                    source = yield Interpreted("", sys.ps2, source.split("\n"))
                    code = interpreter.compile(source, filename, symbol)

            except (OverflowError, SyntaxError, ValueError):
                # Case 1
                interpreter.showsyntaxerror(filename)
            else:
                interpreter.runcode(code)

    except KeyboardInterrupt:
        yield("\nKeyboardInterrupt\n", "" ,[source.split("\n")] if source else [])


def replator(readfunc=None, local=None):
    raw_input = input
    raw_output = sys.stdout.write
    raw_error = sys.stderr.write
    if readfunc is not None:
        raw_input = readfunc
    else:
        try:
            import readline
        except ImportError:
            pass

    session = interpretator()

    # starting the interpreter
    out, prompt, unused = session.send(None)
    raw_output(out)
    while 1:
        try:
            # TODO : format/correct previously displayed input
            try:
                line = raw_input(prompt)
            except EOFError:
                raw_output.write("\n")
                break
            else:
                out, prompt, unused = session.send("\n".join(unused + [line]))
                # TODO : format/correct line even if execution was successful
        except KeyboardInterrupt:
            raw_error("\nKeyboardInterrupt\n")



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # parser.add_argument('-q', action='store_true', help="don't print version and copyright messages")
    args = parser.parse_args()
    # if args.q or sys.flags.quiet:
    #     banner = ''
    # else:
    #     banner = None

    replator()
