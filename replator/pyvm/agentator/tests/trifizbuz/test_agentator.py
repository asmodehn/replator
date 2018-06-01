import io

from . import trifizbuzator
from replator.pyvm.agentator import agentator

agented_trifizbuzator = agentator(instream= io.StringIO(), outstream=io.StringIO())(trifizbuzator)


def test_agented_trifizbuzator():

    tfb = agented_trifizbuzator()
    for e in expected:
        ptyprocess.PtyProcessUnicode()
        assert next(tfb) == str(e)
