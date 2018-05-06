import os
from lark import Lark, InlineTransformer


# TODO : lark grammar importer

class CalculateTree(InlineTransformer):
    from operator import add, sub, mul, truediv as div, neg
    number = float

    def __init__(self):
        self.vars = {}

    def assign_var(self, name, value):
        self.vars[name] = value
        return value

    def var(self, name):
        return self.vars[name]


with open(os.path.join(os.path.dirname(__file__), "calc.lark")) as f:
    interp = Lark(f, parser='lalr', transformer=CalculateTree()).parse

# to be able to test basic parsing functionality
if __name__ == '__main__':
    while True:
        try:
            s = input('> ')
        except EOFError:
            break
        print(interp(s))

