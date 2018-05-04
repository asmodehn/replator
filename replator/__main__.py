import sys

import replator.display

import click

"""
A Terminal interface to your OS, specialized for stack-based languages.
"""


def main():
    try:
        name = sys.argv[1]
        assert open(name, "a")
    except:
        sys.stderr.write(__doc__)
        return
    replator.display.Display(name).main()


if __name__=="__main__":
    main()
