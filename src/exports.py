import sys


def is_debug():
    gettrace = getattr(sys, "gettrace", None)
    if gettrace is None:
        print("No sys.gettrace")
        return
    elif gettrace():
        print("Debug build")
        return True
    else:
        print("Release build")
        return False
