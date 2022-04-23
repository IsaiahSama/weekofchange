import sys

v = sys.version_info
if not (v.major >= 3 and v.minor >= 10):
    print("Python 3.10+ is required to use this program. Please update your python installation and try again")
    input("Press enter to close:")
    raise SystemExit

try:
    import mechanics
except ImportError as err:
    print("Missing libraries:",err)
    input("Press enter to close: ")
    raise SystemExit


class Main:
    """The main class for the program.
    
    Attrs:
    
    Methods:
        main(): The main method of the Program.
        """

    def __init__(self) -> None:
        self.utils = mechanics.Utils()
        self.schedule = mechanics.Schedule(self.utils)

    def main(self):
        """The main method of the program. Controls the main flow!"""
        self.utils.setup()
        self.schedule.load_schedule()


if __name__ == "__main__":
    main = Main()
    main.main()
