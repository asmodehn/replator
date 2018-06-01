"""
Test using the python VM internally, in the same interpreter.
"""
import io
from contextlib import redirect_stderr, redirect_stdout

from ..pyvm import interact



def test_interact():
    strout = io.StringIO()
    strerr = io.StringIO()

    def readfunc(prompt):
        # simulating raw input
        strout.write(prompt)
        yield "a = b + 12"
        yield "\0"

    with redirect_stderr(strerr), redirect_stdout(strout):
        interact(banner="test_repl", readfunc=readfunc, local={'b':30})

    assert strout
    assert strerr
