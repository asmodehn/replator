import pytest

from ..stack import Stack

# TODO : hypothesis

def test_push_from_empty():
    s = Stack(maxlen=8)
    s.push(42)

    assert len(s) == 1
    assert s.pop() == 42


def test_push_from_full():
    s = Stack(range(0, 8), maxlen=8)
    assert len(s) == 8

    # NO ERROR : information was lost
    s.push(42)

    assert len(s) == 8


def test_pop_from_full():
    s = Stack(range(0, 8), maxlen=8)
    assert len(s) == 8

    assert s.pop() == 7
    assert s.pop() == 6
    assert s.pop() == 5
    assert s.pop() == 4
    assert s.pop() == 3
    assert s.pop() == 2
    assert s.pop() == 1
    assert s.pop() == 0

    assert len(s) == 0


def test_pop_from_empty():
    s = Stack(maxlen=8)
    with pytest.raises(IndexError) as excinfo:
        s.pop()

    assert str(excinfo.value) == 'pop from an empty deque'


if __name__ == "__main__":
    pytest.main(['-s'])
