#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import os
from lark import Lark, InlineTransformer

__path__ = os.path.dirname(__file__)

with open(os.path.join(__path__, "lamb.lark")) as f:
    lamb_grammar = Lark(f, parser='lalr', start='file_input')


class LambTree(InlineTransformer):

    def __init__(self):
        self._names = {}

    def defn(self, name, value):
        self._names[name] = value
        return value

    def apply(self, expr):
        return

    def abst(self, vars, expr):
        return

    def vars(self):
        return

    def term(self):
        return


# Note : the transformer needs to be somehow compatible with the runtime...
# TODO : maybe grammar and transformer could be given by the runtime somehow ??? (even remotely ?)

lamb_parser = Lark(lamb_grammar, parser='lalr', transformer=LambTree())

# to be able to test basic parsing fuctionality
if __name__ == '__main__':
    while True:
        try:
            s = input('> ')
        except EOFError:
            break
        print(lamb_parser.parse(s))
