import os

import palimport

with palimport.LarkImporter():
    if __package__:
        from . import bfck
    else:
        import bfck

# to be able to test basic parsing functionality
if __name__ == '__main__':
    while True:
        try:
            s = input('> ')
        except EOFError:
            break
        print(bfck.parser.parse(s).pretty())

