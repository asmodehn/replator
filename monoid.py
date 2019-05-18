"""
Intuitionistic Type Theory as theory of behaviour / Computational Type Theory

Interpretation : function application as a step through time, with minimal "data/complexity" space.

Keep a Categorical perspective

Note also the relationship with Map Theory (Grue)

"""
import copy
import typing
from collections import namedtuple
from dataclasses import dataclass

# define a step, ie function application
# via church encodings for 0 and 1

### debug
def step(x):
    return x + '*'

start = ''

###

ZERO = lambda f: lambda x: x
ONE = lambda f: lambda x: f(x)


# hack test
#print(ONE(step)(start))
assert '*' == ONE(step)(start)

# Peano

SUCC = lambda n: lambda f: lambda x: f(n(f)(x))

assert '**' == SUCC(ONE)(step)(start)

TWO = SUCC(ONE)
THREE = SUCC(TWO)

# Monoid

ADD = lambda n: lambda m: m(SUCC)(n)
# print(ADD(THREE)(TWO)(step)(start))
assert '*****' == ADD(THREE)(TWO)(step)(start)

FOUR = ADD(TWO)(TWO)
FIVE = ADD(THREE)(TWO)

# Semiring

MUL = lambda n: lambda m: lambda f: n(m(f))
# TODO : Think about implementation without implying f
#  Here we use the actual representation (via f) -> not fully abstract over "data/model"...)
#print(MUL(THREE)(TWO)(step)(start))
assert '******' == MUL(THREE)(TWO)(step)(start)




# tuple as 1-arg function representation (1 level for storage) ...

Record = namedtuple( "Record", ["name", "value"])

def ref(r:Record):
    return r.name

def deref(r: Record):
    return r.value


# Orthogonally

Process = namedtuple("Process", ["input", "outpt"])

def args(p: Process):
    return p.input

def impl(p:Process):
    return p.outpt

def eval(p:Process):


    def newin(*args):
        for o in p.outpt:
            for i, a in zip(list(p.input), args):
                if o == i:
                    yield

    def newout(*args):


    def app(*args):
        for o in p.outpt:
            for i, a in zip(list(p.input), args):
                if o == i:
                    yield Process(input=a, output=)
                    break

    return Process(input=, outpt=)

    return lambda a: "".join(app(*a))  # splitting arguments

# Memory space (-> time)
a = Record("answer", "fortytwo")

assert ref(a) == "answer"
assert deref(a) == "fortytwo"

# Compute Space (-> time)
p = Process("answer", "answre")

assert args(p) == "answer"
assert impl(p) == "answre"


# Same number of args
assert eval(p)("abcdef") == "abcdfe", eval(p)("abcdef")
# less

# more









class CharFun:
    repr: str
    impl: typing.Callable

    def __init__(self, repr):
        # copy is implementation detail here
        self.repr = copy.copy(repr)

        def eval(*args):  # evaluation strategy

            args = [a for a in args if a.isalpha()]

            # full eval
            res = []
            for idx, num in enumerate(repr):
               res[idx] = args[num]

            # TODO : step eval
            # TODO : iterator ? generator ? async ?

            return CharFun(repr=res + [args][len(repr):])

        self.impl = eval(repr)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return self.repr

    def __call__(self, *args, **kwargs):
        return self.impl(*args, **kwargs)




NOOP = CharFun(0)
ID = CharFun(1)
APP = CharFun(1,2)





# Interface to replace step and start

import cmd, sys

class MonoShell(cmd.Cmd):
    """
    One character variables only !
    """
    intro = 'Welcome to the time stepper.   Type help or ? to list commands.\n'
    prompt = '(timestep) '
    file = None

    ZERO = lambda f: lambda x: x
    ONE = lambda f: lambda x: f(x)
    # Peano
    SUCC = lambda n: lambda f: lambda x: f(n(f)(x))

    def __getattr__(self, item):
        # dynamically populating scope
        if item.startswith('do_'):
            i = item[3:]
            if len(i) == 1:  # one char is definition
                def mutate(arg):
                    setattr(self, item, CharFun(repr = arg))
                return mutate
            else:  # otherwise : application/reduction (1 time)
                return CharFun(item[3:])


        else:
            raise NotImplementedError(item)

    def do_zero(self, arg):
        args = arg.split()
        self.named['_'] = args[1:]
        print(self.named['_'])

    def do_one(self, arg):
        args = arg.split()
        self.named['_'] = map(args[0], args[1:])
        print(self.named['_'])

    def do_let(self, arg):
        args = arg.split()
        self.named[arg[0]] = arg[1:]
        self.named['_'] = arg[0]  # Note :chain of dereference, different from function app ??
        print(self.named['_'])

    def do_bye(self, arg):
        'exit:  BYE'
        print('Thank you for using MonoShell')
        self.close()
        return True

    def precmd(self, line):
        line = line.lower()
        if self.file and 'playback' not in line:
            print(line, file=self.file)
        return line

    def close(self):
        if self.file:
            self.file.close()
            self.file = None


if __name__ == '__main__':
    MonoShell().cmdloop()
