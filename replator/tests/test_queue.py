import pytest

from ..queue import Queue


# TODO : hypothesis

def test_enqueue_from_empty():
    q = Queue(maxlen=8)
    q.enq(42)

    assert len(q) == 1
    assert q.deq() == 42


def test_enqueue_from_full():
    q = Queue(range(0, 8), maxlen=8)
    assert len(q) == 8

    # NO ERROR : information was lost
    q.enq(42)

    assert len(q) == 8


def test_dequeue_from_full():
    q = Queue(range(0, 8), maxlen=8)
    assert len(q) == 8

    assert q.deq() == 0
    assert q.deq() == 1
    assert q.deq() == 2
    assert q.deq() == 3
    assert q.deq() == 4
    assert q.deq() == 5
    assert q.deq() == 6
    assert q.deq() == 7

    assert len(q) == 0


def test_dequeue_from_empty():
    q = Queue(maxlen=8)
    with pytest.raises(IndexError) as excinfo:
        q.deq()

    assert str(excinfo.value) == 'pop from an empty deque'


if __name__ == "__main__":
    pytest.main(['-s'])
