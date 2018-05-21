import os

import palimport

with palimport.LarkImporter():
    print(__package__)
    if __package__:
        from . import calc
    else:
        import calc

# to be able to test basic parsing functionality
if __name__ == '__main__':
    while True:
        try:
            s = input('> ')
        except EOFError:
            break
        print(calc.parser.parse(s).pretty())

