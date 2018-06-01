
from . import trifizbuzator
from replator.pyvm.agentator import agentator

# trifizbuzator but as a process
agented_trifizbuzator = agentator()(trifizbuzator)

if '__main__' == __name__:
    # this process starts looping and in/output to streams...
    agented_trifizbuzator()
