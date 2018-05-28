"""Basic Forth Interpreter

Forth being completely dynamic make the parsing/interpreting distinction kind of awkward.
Syntax can change at the whim of the programmer.

This is heavily inspired by http://www.exemark.com/FORTH/eForthOverviewv5.pdf

This modules defines a ... TODO
that emulates a VFC in python, using the running python interpreter (TODO : AST - dis)
"""
from queue import LifoQueue

#  TODO : meta class to fill up VFC dictionary depending on previously imported forth modules
# TODO : or anything else modifying the behavior of any following VFC instantiation
class VFC(object):
    """
    Forth is a computer model which can be implemented on any real CPU with reasonable resources.  This model is often called a
    virtual Forth computer.  The minimal components of a virtual Forth computer are:
    1.   A dictionary in memory to hold all the execution procedures.
        -> This will be our class __dict__
    2.   A return stack to hold return addresses of procedures yet to be executed.
        -> This will be usual python call semantics
    3.   A data stack to hold parameters passing between procedures.
        -> This will be usual python call semantics
    4.   A user area in RAM memory to hold all the system variables.
        -> This will be a local mem attribute
    5.   A CPU to move date among stacks and memory, and to do ALU operations to parameters stored on the data stack.
        -> this will be our python interpreter
    """

    #: BYE returns control from Forth back to the operating system.
    BYE= 'BYE'
    #: !io initializes the serial I/O device in the system so that it can interact with the user through a terminal.
    IO= '!io'
    #: ?rx is used to implement ?KEY and KEY, and tx! is used to implement EMIT. eForth communicates with the user
    #: through these words which supports terminal interactions and file download/upload.  Here these words are
    #: defined using the DOS service calls.  For embedded controllers, these three words must
    #: be defined for the specific I/O devices.
    RX= '?rx'
    TX= 'tx!'

    def __init__(self):
        """
        Building the Virtual Forth Computer
        """
        self.mem = dict()
        self.data = LifoQueue()
        self.ret = LifoQueue()

        # TODO : some of these are not needed...
        #: Interpreter Pointer
        #self.ip = 0
        # taken care of by iterable and next

        #: Data Stack Pointer
        #self.sp = 0
        #: Return Stack Pointer
        #self.rp = 0
        # managed by stack implementation

        #: Word or Work Pointer
        self.wp = 0
        #: User Area Pointer
        self.up = 0


    def __enter__(self):
        """
        Starting the Virtual Forth Computer.
        CAn itbe the repl context ?
        Can also been seen as forth's "compiling" ?
        """

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Shutting the Virtual Forth Computer down.
        """

    def __call__(self, *words, **defined_words):
        """
        The list processing subroutine.
        It is the "eval" of forth.
        :param args: the iterable of forth words to evaluate
        :param kwargs: additional dictionary definition for this call only
        :return:
        """

        for word in words:

            if BYE == word



def interp():

    AST = calc.parser.parse(s)
    pysource = CalculatePython().transform(AST)
    # TODO : fix that in the grammar
    if not isinstance(pysource, (str,)):
        pysource = str(pysource)
    return pysource

