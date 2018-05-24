import os

import palimport

with palimport.LarkImporter():
    if __package__:
        from . import hier
    else:
        import hier

from lark.reconstruct import Reconstructor
from lark.tree import Tree


def dir2tree():
    cwdtree = Tree(os.getcwd(), os.listdir(os.getcwd()))
    tree = cwdtree
    for path, dirs, files in os.walk(os.getcwd()):
        tree = Tree(path, files)



# to be able to test basic constructing functionality
if __name__ == '__main__':

    tree = dir2tree()

    new_json = Reconstructor(hier.parser).reconstruct(tree)

    while True:
        try:
            s = input('> ')
        except EOFError:
            break
        print(hier.parser.parse(s).pretty())

