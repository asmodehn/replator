"""
A simple Python VM, in the spirit of other minimal languages out here :

0) Starts up (optionally as an external process, in a sandbox, etc.)
1) Accept strings in python syntax for evaluation
2) Accepts socket connections for code injection and remote debugging (via manhole)
3) Shutsdown and cleanup after itself

"""

