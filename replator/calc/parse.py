import os
from lark import Lark, InlineTransformer

# TODO : lark grammar importer

with open(os.path.join(os.path.dirname(__file__), "calc.lark")) as f:
    parse = Lark(f, parser='lalr').parse

# to be able to test basic parsing functionality
if __name__ == '__main__':
    while True:
        try:
            s = input('> ')
        except EOFError:
            break
        print(parse(s).pretty())

