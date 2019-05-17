"""
Intuitionistic Type Theory as theory of behaviour / Computational Type Theory

Interpretation : function application as a step through time, with minimal "data/complexity" space.

Keep a Categorical perspective

Note also the relationship with Map Theory (Grue)

"""


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




# Interface to replace step and start

import cmd, sys

class MonoShell(cmd.Cmd):
    intro = 'Welcome to the time stepper.   Type help or ? to list commands.\n'
    prompt = '(timestep) '
    file = None

    ZERO = lambda f: lambda x: x
    ONE = lambda f: lambda x: f(x)
    # Peano
    SUCC = lambda n: lambda f: lambda x: f(n(f)(x))

    named = {}

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
