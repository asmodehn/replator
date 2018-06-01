"""
A decorator that transform a generator into an agent by:
- redirecting input, output, errors
-

"""
import io
import sys

import wrapt


def agentator(instream = sys.stdin, outstream = sys.stdout, lineprompt="...", formprompt=">>>", maxcycles = 1000):
    """
    Returns decorator that transforms a generator into a producer/consumer of stream data
    It is still conceptually a generator, however yielding is now done when waiting for data, signaled through a prompt in the outstream.
    Errors/Exceptions are handled out of band (can be passed in the same stream, in another stream, in a log, etc.)
    The goal is to be able to plug a terminal (pty) into an agentator and have it working out of the box.
    """
    cycles = 0

    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):

        w = wrapped(*args, **kwargs)
        w.send(None)
        cycles = 0
        while 0 < cycles < maxcycles:  #TODO : add "infinite" detection... or maybe not ?
            inp = instream.read()
            # default value
            inp = inp if inp else 1  # initial input data ( or nothing, or loop forever, etc.)
            yielded = w.send(inp)
            # TODO : serializer / lexing
            # TODO : allow introspection...
            out = str(yielded)
            outstream.write(out)
            cycles += 1

    return wrapper, cycles  # instrumenting the generator

#TODO : instrumenting be a function ???


def nextator(instream = sys.stdin, outstream = sys.stdout, errstream = sys.stderr):
    """Inverse semantics of the agentator
    returns a decorator that transform a producer/consumer of stream data into a generator"""
    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        # TODO
        w = wrapped(*args, **kwargs)




def terminator():
    from blessings import Terminal
    # creating a terminal
    term = Terminal()
    print('All your {t.red}base {t.underline}are belong to us{t.normal}'.format(t=term))






if '__main__' == __name__:
    agented_trifizbuzator()
