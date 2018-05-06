import pytest
from lark import Lark
import os
from ..parse import parse


def test_calc_add():

    assert parse("3 + 2", ).pretty() == """add
  number\t3
  number\t2
"""


def test_calc_sub():

    assert parse("3 - 2", ).pretty() == """sub
  number\t3
  number\t2
"""


def test_calc_mul():

    assert parse("3 * 2", ).pretty() == """mul
  number\t3
  number\t2
"""


def test_calc_div():

    assert parse("3 / 2", ).pretty() == """div
  number\t3
  number\t2
"""


def test_calc_assign():

    assert parse("b = 2", ).pretty() == """assign_var
  b
  number\t2
"""








if __name__ == '__main__':
    pytest.main(['-s'])
