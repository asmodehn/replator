import pytest
from lark import Lark

from .. import parse

calc_parser = Lark(parse.calc_grammar, parser='lalr')


def test_calc_add():

    assert calc_parser.parse("3 + 2", ).pretty() == """add
  number\t3
  number\t2
"""


def test_calc_sub():

    assert calc_parser.parse("3 - 2", ).pretty() == """sub
  number\t3
  number\t2
"""


def test_calc_mul():

    assert calc_parser.parse("3 * 2", ).pretty() == """mul
  number\t3
  number\t2
"""


def test_calc_div():

    assert calc_parser.parse("3 / 2", ).pretty() == """div
  number\t3
  number\t2
"""


def test_calc_assign():

    assert calc_parser.parse("b = 2", ).pretty() == """assign_var
  b
  number\t2
"""








if __name__ == '__main__':
    pytest.main(['-s'])
