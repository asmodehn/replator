
"""
A basic stack implementation in python

TODO : produce bytecode doing the job, dynamically with pypy, with more awesomeness.
"""


#TODO : import contracts

from collections import deque


class Stack(deque):

    def push(self, data):
        self.append(data)

    # stack pop and deque pop are the same




