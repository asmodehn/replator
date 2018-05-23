import os

import palimport

with palimport.LarkImporter():
    if __package__:
        from . import hier
    else:
        import hier

# to be able to test basic parsing functionality
if __name__ == '__main__':
    while True:
        try:
            s = input('> ')
        except EOFError:
            break
        print(hier.parser.parse(s).pretty())

