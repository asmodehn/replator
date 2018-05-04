
"""
A basic queue implementation in python

TODO : produce bytecode doing the job, dynamically with pypy, with more awesomeness.
"""

#TODO : import contracts

from collections import deque


class Queue(deque):

    def enq(self, data):
        self.append(data)

    def deq(self):
        return self.popleft()

