"""File responsible for most of the mechanics that will be used throughout this program."""

from dataclasses import dataclass, field
import os
import pyttsx3
import time
import errors

from config import load_yaml

config = load_yaml()


@dataclass
class Constants:
    days:list = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
    folder_path: str = config["folder_location"]
    speech_rate: int = config["text_to_speech"]['rate']
    speech_volume: float = config["text_to_speech"]['volume']
    speech_voice: int = config["text_to_speech"]['voice']

class Utils:
    """Class used to handle all of the major utility functions that this program will use.
    
    Attrs:
        
    Methods:
        setup(): Used to setup all data that the program will need to function.
        get_file_name(day:str): Returns the path to the file matching the given day
        get_current_day(): Returns the current day as a title cased String.
    """

    def __init__(self) -> None:
        self.speech = Speech()

    def setup(self):
        """Method used to setup the data that the program needs to function."""

        if not os.path.exists(Constants.folder_path):
            try:
                os.mkdir(Constants.folder_path)
            except Exception as err:
                print("An error occurred while trying to make the required files:", err)
                raise SystemExit

        for day in Constants.days:
            day_file = self.get_file_name(day)
            if os.path.exists(day_file): continue
            with open(day_file, "w") as fp:
                fp.write(f"# {day}'s schedule goes here. Format: time_in_24_hours: task")

        self.speech.say_and_print("Everything has been setup correctly!!")

    def get_file_name(self, day:str):
        """Returns the path to the filename matching the given day.
        
        Args:
            day (str): The day whose filepath is requested."""

        return os.path.join(Constants.folder_path, day + ".txt")

    def get_current_day(self):
        """Returns the current day."""
        short_day = time.ctime().split(" ")[0]
        for day in Constants.days:
            if day.startswith(short_day.title()):
                return day 
        raise errors.NonExistentDay(short_day, "\nctime bugging?")

class Speech:
    """Class responsible for the setup and handling of the Text To Speech
    
    Attrs:
        engine: The Text to speech engine being used
    Methods:
        setup(): Used to setup the Text To Speech.
        say(message:str): Used to speak a given message.
        say_and_print(message:str): Prints a message to the screen, and says it as well."""

    def __init__(self) -> None:
        self.engine = None
        self.setup()

    def setup(self):
        self.engine = pyttsx3.init()
        
        self.engine.setProperty('rate', Constants.speech_rate)
        self.engine.setProperty('voice', Constants.speech_voice)
        self.engine.setProperty('volume', Constants.speech_volume)

    def say(self, message:str):
        """Method that uses text to speech to read out a given message.
        
        Args:
            message(str): The message to be read."""

        self.engine.say(message)
        self.engine.runAndWait()

    def say_and_print(self, message:str):
        """Used to display a message to the screen, and read it out loud as well.
        
        Args:
            message(str): The message to be displayed and read."""

        print(message)
        self.say(message)

class Schedule:
    """Class which actually manages everything relating to the schedule keeping.
    
    Attrs:
        utils (Utils) 
        tasks(dict): The schedule for the current day.
    Methods:
        load_schedule(): Method used to load the current day's schedule into memory
    """

    def __init__(self, utils:Utils) -> None:
        self.utils = utils
        self.tasks = {}

    def load_schedule(self):
        """Method used to load the current schedule into memory."""
        current_day = self.utils.get_current_day()

        filename = self.utils.get_file_name(current_day.title())
        with open(filename) as fp:
            lines = fp.readlines()
        
        tasks = {}
        for line in lines:
            if not line or line.startswith("#"): continue
            try:
                line = line.strip()
                start_time = line.split(':')[0]
                if not start_time.isnumeric(): raise errors.BadDayInformation(line, filename, f"Provided time, {start_time} was not a number.")
                start_time = int(start_time)
                task = ':'.join(line.split(":")[1:])
            except Exception as err:
                raise errors.BadDayInformation(line, filename, err)
            
            tasks[start_time] = task

        self.tasks = tasks
        print(tasks)

