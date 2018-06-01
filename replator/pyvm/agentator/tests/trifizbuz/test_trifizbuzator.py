
from .trifizbuzator import trifizbuzator


expected = [1, 2, "tri", 4, "fizz", "tri", "buzz", 8, "tri", "fizz",
                11, "tri", 13, "buzz", "tri", 16, 17, "tri", 19, "fizz",
                "tri", 22, 23, "tri", "fizz", 26, "tri", "buzz", 29, "tri",
                31, 32, "tri", 34, "fizz", "tri", 37, 38, "tri", "fizz",
                41, "tri"]

def test_trifizbuzator():

    tfb = trifizbuzator()
    tfb.send(None)  # start
    for i, e in zip(range(1, 43), expected):
        assert tfb.send(i) == e

