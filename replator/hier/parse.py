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
        # note the outputted tree can be interpreted in different ways :
        # - as a constraint to be checked for
        # - as a declarative programming : this is the file hierarchy that we want (maybe to create a VM, etc.)
        # - more ?
