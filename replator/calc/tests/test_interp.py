import pytest
from lark import Lark

from ..interp import interp

# Testing Parsing with inline transformation
# In our case here, it does computation


def test_calc_add():

    assert interp("3 + 2", ) == 5.0


def test_calc_sub():

    assert interp("3 - 2", ) == 1.0


def test_calc_mul():

    assert interp("3 * 2", ) == 6.0


def test_calc_div():

    assert interp("3 / 2", ) == 1.5


def test_calc_assign():

    assert interp("b = 2", ) == 2








if __name__ == '__main__':
    pytest.main(['-s'])
