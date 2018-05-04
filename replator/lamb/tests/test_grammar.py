import pytest
from lark import Lark

from .. import parse

lamb_parser = Lark(parse.lamb_grammar, parser='lalr')


def test_term():
    assert lamb_parser.parse("a", ).pretty() == """term\ta
    """


def test_abst():
    assert lamb_parser.parse("lambda x : x y", ).pretty() == """lambda
    var\tx
    expr
      term\tx
      term\ty
    """

def test_appl():
    assert lamb_parser.parse("(x y)", ).pretty() == """apply
    expr
      term\tx
      term\ty
    """


def test_defn():
    assert lamb_parser.parse("(define id (\ x : x))", ).pretty() == """define
    id
    abst
      term\tx
      expr
        term\tx
    """


if __name__ == '__main__':
    pytest.main(['-s'])
