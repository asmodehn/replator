import io
import sys
import argparse
import code
import traceback
from contextlib import redirect_stdout, redirect_stderr, wraps
from codeop import CommandCompiler, compile_command
from collections import namedtuple
import inspect

# Inspired by Python's code module
# With a somewhat different design :
# The interpretator class is a isolated instance
# and allows only one in/out stream connection to it.

Interpreted = namedtuple("Interpreted", ["out", "prompt", "unused"])

#  we need a minimal format for two sides to agree whose turn it is to receive / send
# if we make the receive implicit. format is output only: "here is the data" data = None or data->send.
# Which implies a character model... Sending every character as it is typed & displaying as it is received.
# On the other hand having a line model, implies some structure of the code, which makes it less generic.
#
# We probably do want some structure, for simplicity or reading input mixed with output.
# a minimal grammar that we can define can be the EOF character representing the end of communication.
# from input (client/pty master) it means we are done, disconnect input. But server doesnt care about that.
# from output (server/pty slave) it means job/output finished, back to master. Only client cares.
#
# Trick : in the perspective that interpreter can change the inputed text we hav to define some kind of universal protocol to modify text.
# It could also be used in the concept of storing change made to sourcecode (see http://expressionsofchnge.org)
# The interpreter assumes some minimal capabilities by the terminal.
# We'll try to stick to standard ASCII ( and usual C escape sequences ), even though we aim to support unicode.

#  Goal is to store modifictions, or run modifications, onthe input string...
TerminalControlGrammar = namedtuple("ControlGrammar", [
    "LEFT",   # moves cursor back
    "UP",   # moves cursor up
    "RIGHT",   # moves cursor right
    "DOWN",   # moves cursor down
])
# TODO : check "terminal whispering" to find libraries abstracting terminal types...


#: defining the characters that are prompts, and give back the control to the client/terminal
Prompts = namedtuple("Prompts", ["char", "line", "form"])

try:
    sys.ps1
except AttributeError:
    sys.ps1 = ">>> "
try:
    sys.ps2
except AttributeError:
    sys.ps2 = "... "

py_prompts = Prompts(char="", line="\n" + sys.ps2, form="\n" + sys.ps1)
# char prompt == cursor ?
# string syntax for this ??

# TODO : check ptyprocess
input = io.StringIO()
output = io.StringIO()
errors = io.StringIO()



# TODO : decorator as stream operator (see FRP)
# TODO : one needs to grab stdin out and err from the environment, and plug them to kwargs for it. function will need to input output there.
# TODO : one needs to redirect stdin, out and err. better if we can reuse existing ones.
# TODO : one might be needed to switch between a stderr + stdout process model, to a pty model (one in one out)


def line_interpretator(interpreter = code.InteractiveInterpreter(), filename="<input>", symbol="single"):
    code = interpreter.compile("pass", filename, symbol)  #  noop
    try:
        source = yield Interpreted(banner if banner else "", sys.ps1, [])
        banner = None  # consume banner
        while source:
            code = interpreter.compile(source, filename, symbol)
            # Case 2 : need more lines !!
            if code is None:
                # TODO : return formatted source
                source = yield Interpreted("", sys.ps2, source.split("\n"))
            else:
                source = None
                break
    except (OverflowError, SyntaxError, ValueError):
        # Case 1
        interpreter.showsyntaxerror(filename)
    else:
        interpreter.runcode(code)



# Note : such a generator is semantically similar to a (minimal) interactive program...
# with the user giving input and waiting for output.
# TODO : find a way to integrate that in command line...
def interpretator(interpreter = code.InteractiveInterpreter(), filename="<input>", symbol="single"):
    """Interpretator : A Python Interpreter as an output generator"""

    yield py_prompts

    cprt = 'Type "help", "copyright", "credits" or "license" for more information.'
    banner = "%s\nPython %s on %s\n%s\n" % (interpretator.__doc__, sys.version, sys.platform, cprt, )

    try:
        code = interpreter.compile("pass", filename, symbol)  #  noop
        try:
            source = yield Interpreted(banner if banner else "", sys.ps1, [])
            banner = None  # consume banner
            while source:
                code = interpreter.compile(source, filename, symbol)
                # Case 2 : need more lines !!
                if code is None:
                    # TODO : return formatted source
                    source = yield Interpreted("", sys.ps2, source.split("\n"))
                else:
                    source = None  # consume source
                    break
        except (OverflowError, SyntaxError, ValueError):
            # Case 1
            interpreter.showsyntaxerror(filename)
        else:
            interpreter.runcode(code)

    except KeyboardInterrupt:
        yield("\nKeyboardInterrupt\n", "" ,[source.split("\n")] if source else [])


# find the strict minimum for this to interface interpretator directly  with command line/pty...
# TODOD : a decorator for interactive generators...
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
