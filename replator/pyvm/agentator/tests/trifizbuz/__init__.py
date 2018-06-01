# potentially infinite interactive generator for testing
def trifizbuzator():
    cur = 1
    while True:

        if cur % 3 == 0:
            cur = yield "tri"
        elif cur % 5 == 0:
            cur = yield "fizz"
        elif cur % 7 == 0:
            cur = yield "buzz"
        else:
            cur = yield cur

        cur = int(cur)  # parser step


