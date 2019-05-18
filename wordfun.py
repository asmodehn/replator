import cmd
import copy
import typing
import functools


def process(input: typing.Set[str], output: typing.List[str]):

    input = list(set(input))  # to enforce unicity

    # Application
    def procimpl(args: typing.List[str]):

        resin = []
        resout = []

        for o in output:
            if o in input:  # bound variable
                found = False
                for i, a in zip(input, args):
                    if o == i:
                        found = True
                        resout.append(a)
                        break
                if not found:
                    resout.append(o)  # remaining var from partial apply
            else:
                resout.append(o)  # free variable

        # partial application
        for i in input[len(args):]:
            resin.append(i)

        # over application
        for a in args[len(input):]:
            resout.append(a)

        if resin:  # partial application
            return process(resin, resout)  # recursion ??
        else:
            return resout

    return procimpl


K = process(["x", "y"], ["x"])
C = process(["x", "y", "z"], ["x", "z", "y"])
W = process(["x", "y"], ["x", "y", "y"])

# correct arg number
assert K(["allo", "bob"]) == ["allo"]
assert W(["allo", "bob"]) == ["allo", "bob", "bob"]
assert C(["allo", "bob", "wazzup"]) == ["allo", "wazzup", "bob"]

# partial apply
assert K(["allo"])(["bob"]) == ["allo"]
assert W(["allo"])(["bob"]) == ["allo", "bob", "bob"]
assert C(["allo"])(["bob", "wazzup"]) == ["allo", "wazzup", "bob"]

# over apply
assert K(["allo", "bob", "and", "jack"]) == ["allo", "and", "jack"]
assert W(["allo", "bob", "and", "jack"]) == ["allo", "bob", "bob", "and", "jack"]
assert C(["allo", "bob", "wazzup", "and", "jack"]) == ["allo", "wazzup", "bob", "and", "jack"]





# Note : def is a feature of the repl, not the language itself.

class WordShell(cmd.Cmd):
    """
    One character variables only !
    """
    intro = 'Welcome to the time stepper.   Type help or ? to list commands.\n'
    prompt = '(timestep) '
    file = None

    proc_store = {}

    def do_def(self, arg):
        args = arg.split()
        # TODO : find a better way than partial app here (multiline ?)
        self.proc_store[args[0]] = functools.partial(process, input=args[1:])

    def do_impl(self, arg):
        args =arg.split()
        # TODO : find a better way than partial app here (multiline ?)
        self.proc_store[args[0]] = self.proc_store[args[0]](output=args[1:])

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
    WordShell().cmdloop()
