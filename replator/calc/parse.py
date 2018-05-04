
from lark import Lark, InlineTransformer

calc_grammar = """
    ?start: sum
          | NAME "=" sum    -> assign_var

    ?sum: product
        | sum "+" product   -> add
        | sum "-" product   -> sub

    ?product: atom
        | product "*" atom  -> mul
        | product "/" atom  -> div

    ?atom: NUMBER           -> number
         | "-" atom         -> neg
         | NAME             -> var
         | "(" sum ")"

    %import common.CNAME -> NAME
    %import common.NUMBER
    %import common.WS_INLINE

    %ignore WS_INLINE
"""

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


calc_parser = Lark(calc_grammar, parser='lalr', transformer=CalculateTree())


def main():
    while True:
        try:
            s = input('> ')
        except EOFError:
            break
        print(calc_parser.parse(s).pretty())


# to be able to test basic parsing fuctionality
if __name__ == '__main__':
    main()

