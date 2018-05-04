"""
The Runtime Environment.
Accepting only delimited continuation
"""

import asyncio

# This breaks input ??
# async def foo():
#     print('Running in foo')
#     await asyncio.sleep(0)
#     print('Explicit context switch to foo again')
#
#
# async def bar():
#     print('Explicit context to bar')
#     await asyncio.sleep(0)
#     print('Implicit context switch back to bar')
#
#
#
# async def apply(cont, *args):
#     await cont(*args)
#
#
# #: the queue of delimited continuation to run (implemented as coroutines)
# conts = asyncio.Queue()
#
#
# # only one event loop in this module
# ioloop = asyncio.get_event_loop()
#
#
#
#
#
#
#
# #tasks = [ioloop.create_task(foo()), ioloop.create_task(bar())]
# #wait_tasks = asyncio.wait(tasks)
#
# # lets run !
# try:
#     ioloop.run_forever()
# finally:
#     ioloop.close()

