import pytest

from ..parse import calc


def test_calc():
    ast1 = calc("a = 1+2")
    assert 3 == ast1
    ast2 = calc("1+a*-3")
    assert -8 == ast2