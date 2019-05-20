import cmd
import copy
import typing
import functools
import itertools

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Trip:

    repr: typing.List[typing.Union[str, 'Trip']]
    # note here the multiple trees, more or less explicitly shown in code.
    # - one for order of argument evaluation
    # - one for syntax for order of application
    # - one for implementation execution (arg implementation order depends on host lang)
    # - one for naming and referencing
    # TODO : check their combination and opetopes rules...
    # TODO : check Trie for implementation down to the character...

    def __post_init__(self):
        """normalize AST representation"""
        normalized_repr = []
        for i, e in enumerate(self.repr):
            if e != "0":
                normalized_repr.append(e)
            else:
                t = Trip(self.repr[i+1:])
                normalized_repr.append(t)
                break  # it ends here. the rest is in subtree.
        object.__setattr__(self, 'repr', normalized_repr)

    def __str__(self):
        # reconstruct as a mean to dynamically check identity
        return "".join(self.repr)

    def __repr__(self):
        return str(self)

    def __call__(self, context: typing.Optional[typing.Dict[str, 'Trip']]):
        """execution of an AST/CFT"""

        context = globals() if context is None else context

        resv_list: typing.List[typing.Callable] = []  # TODO : correctly type callable

        for i in self.repr:
            if i in context:
                resv_list.append(context[i]())

        def impl(args):
            result = []
            for e in resv_list:
                if isinstance(e, str) and e.isdigit():
                    if int(e) < len(args):
                        res = args[int(e)]
                    else:
                        res = str(int(e) - len(args))  # partial application

                    result.append(res)
                elif isinstance(e, Trip):
                    # pass  # What ????

                else:        # overapplication
                    result.append(res)

            return "".join(result)

        return impl



B = Trip(["1", "0", "2", "3"])
K = Trip(["1"])
C = Trip(["1", "3", "2"])
W = Trip(["1", "2", "2"])

# correct arg number
assert K(globals())(["allo", "bob"]) == ["allo"], K(["allo", "bob"])
assert W(globals())(["allo", "bob"]) == ["allo", "bob", "bob"], W(["allo", "bob"])
assert C(globals())(["allo", "bob", "wazzup"]) == ["allo", "wazzup", "bob"], C(["allo", "bob", "wazzup"])

# partial apply
assert K(globals())(["allo"])(["bob"]) == ["allo"]
assert W(globals())(["allo"])(["bob"]) == ["allo", "bob", "bob"]
assert C(globals())(["allo"])(["bob", "wazzup"]) == ["allo", "wazzup", "bob"]

# over apply
assert K(globals())(["allo", "bob", "and", "jack"]) == ["allo", "and", "jack"]
assert W(globals())(["allo", "bob", "and", "jack"]) == ["allo", "bob", "bob", "and", "jack"]
assert C(globals())(["allo", "bob", "wazzup", "and", "jack"]) == ["allo", "wazzup", "bob", "and", "jack"]






def process(output: typing.List[str], context: typing.Optional[typing.Dict[str, typing.Callable]]):
    """
    :param output: representation of the process. similar to its output with 1 2 3 4 denoting argument positions
    :param context: a mutable mapping of processes, to be used / called by this process
    :return:
    """


    # Building AST
    impl = lambda: None

    for i, w in enumerate(reversed(output)):
        if w.isdigit() and w == 0:
            impl = process(output[len(output)-i:], context)



    # Application
    def procimpl(args: typing.List[str]):

        resout = []
        for o in output:
            if o.isdigit():
                assert int(o) is not 0
                if len(args) < int(o):  # bound variable
                    resout.append(args[int(o)])
                    break
                else:  # partial apply -> reindex args
                    resout.append(str(int(o) - len(args)))
            else:
                resout.append(o)  # free variable

        if any(map(lambda s: s.isdigit(), resout)):  # partial application
            return process(resout)  # recursion ??
        else:
            return resout

    return procimpl


B = process(["1", "0", "2", "3"])
K = process(["1"])
C = process(["1", "3", "2"])
W = process(["1", "2", "2"])

# correct arg number
assert K(["allo", "bob"]) == ["allo"], K(["allo", "bob"])
assert W(["allo", "bob"]) == ["allo", "bob", "bob"], W(["allo", "bob"])
assert C(["allo", "bob", "wazzup"]) == ["allo", "wazzup", "bob"], C(["allo", "bob", "wazzup"])

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

    def __getattr__(self, item):
        if item.startswith('do_'):
            return self.proc_store.get(item[3:])
        else:
            raise NotImplementedError

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
