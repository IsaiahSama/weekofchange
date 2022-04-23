import sys

v = sys.version_info
if not (v.major >= 3 and v.minor >= 10):
    print("Python 3.10+ is required to use this program. Please update your python installation and try again")
    input("Press enter to close:")
    raise SystemExit

try:
    pass
except ImportError as err:
    print("Missing libraries:",err)
    input("Press enter to close: ")
    raise SystemExit