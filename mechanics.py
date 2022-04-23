"""File responsible for most of the mechanics that will be used throughout this program."""

from dataclasses import dataclass
import os

from config import load_yaml

config = load_yaml()

@dataclass
class Constants:
    days:list = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
    folder_path: str = config["folder_location"]

class Utils:
    """Class used to handle all of the major utility functions that this program will use.
    
    Attrs:
        
    Methods:
        setup(): Used to setup all data that the program will need to function.
    """

    def __init__(self) -> None:
        pass

    def setup(self):
        """Method used to setup the data that the program needs to function."""

        if not os.path.exists(Constants.folder_path):
            try:
                os.mkdir(Constants.folder_path)
            except Exception as err:
                print("An error occurred while trying to make the required files:", err)
                raise SystemExit

        for day in Constants.days:
            day_file = os.path.join(Constants.folder_path, day + ".txt")
            if os.path.exists(day_file): continue
            with open(day_file, "w") as fp:
                fp.write(f"# {day}'s schedule goes here. Format: time_in_24_hours:task")

        print("Everything has been setup correctly!!")
