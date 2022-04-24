"""File responsible for most of the mechanics that will be used throughout this program."""

import os
import pyttsx3
import time
import errors

from dataclasses import dataclass, field
from config import load_yaml
from threading import Thread

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
        get_current_time(): Returns the current time in 24hr format (1300 instead of 13:00)
        get_twelve_time(): Returns the time in 12 hour format.
        thread_this_func(func, *args): Makes a thread for a passed function and starts it.
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

    def get_file_name(self, day:str) -> str:
        """Returns the path to the filename matching the given day.
        
        Args:
            day (str): The day whose filepath is requested.
            
        Returns:
            str"""

        return os.path.join(Constants.folder_path, day + ".txt")

    def get_current_day(self) -> str:
        """Returns the current day.
        
        Returns:
            str"""
        short_day = time.ctime().split(" ")[0]
        for day in Constants.days:
            if day.startswith(short_day.title()):
                return day 
        raise errors.NonExistentDay(short_day, "\nctime bugging?")

    def get_current_time(self) -> int:
        """Returns the current time.
        
        Returns:
            int"""

        localtime = time.localtime()
        hour, minutes = str(localtime.tm_hour), str(localtime.tm_min)
        if len(hour) <= 1:
            while len(hour) != 2:
                hour = "0" + hour
        if len(minutes) <= 1:
            while len(minutes) != 2:
                minutes = "0" + hour
        return hour + minutes

    def get_twelve_time(self, ftime:int) -> tuple[int, int]:
        """Returns the time in classic 12 hour format"""
        stime = str(ftime)
        hour = stime[:-2]
        minutes = stime[-2:]
        if int(hour) > 12:
            hour = str(int(hour) - 12)
        return hour, minutes

    def thread_this_func(self, func, *args):
        """Makes a thread for the passed function and starts it.
        
        Args:
            func: The function to be threaded.
            *args: Any extra arguments the function may need"""

        thread = Thread(target=func, args=args, daemon=True)
        thread.start()

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
        utils (Utils): An instance of the Utils class.
        tasks(dict): The schedule for the current day.
        times (list): A sorted list of times for the events on the current days
        current_day(str): The current day
    Methods:
        load_schedule(): Method used to load the current day's schedule into memory
        watch_the_clock(): Method used for watching the clock, to determine when a new day has begun 
        track(): Used to track the schedule for the current day.
    """

    def __init__(self, utils:Utils) -> None:
        self.utils = utils
        self.tasks = {}
        self.times = []
        self.current_day = self.utils.get_current_day()
        
    def start_threads(self):
        """All threaded functions for this class that are to be threaded, goes here."""
        self.utils.thread_this_func(self.watch_the_clock)
        self.utils.thread_this_func(self.track)
        
    def load_schedule(self):
        """Method used to load the current schedule into memory."""

        filename = self.utils.get_file_name(self.current_day.title())
        with open(filename) as fp:
            lines = fp.readlines()
        
        tasks = {}
        for line in lines:
            line = line.strip("\n").strip()
            if not line or line.startswith("#"): continue
            try:
                start_time = line.split(':')[0]
                if not start_time.isnumeric(): raise errors.BadDayInformation(line, filename, f"Provided time, {start_time} was not a number.")
                start_time = int(start_time)
                task = ':'.join(line.split(":")[1:])
            except Exception as err:
                raise errors.BadDayInformation(line, filename, err)
            
            tasks[start_time] = task

        self.tasks = tasks
        self.times = sorted(tasks)

    def watch_the_clock(self):
        """Method used to track the current day, and detect when the day changes. Will load the corresponding schedule."""
        while True:
            current_day = self.utils.get_current_day()
            if current_day == self.current_day:
                time.sleep(120)
                continue
            
            self.current_day = current_day
            self.utils.speech.say("It's a new day and a new schedule!")
            self.load_schedule()

    def track(self):
        """Method used to track the schedule for the current day"""
        
        self.times = [time for time in self.times if time >= int(self.utils.get_current_time())]
        while True:
            if not self.times:
                self.utils.speech.say_and_print("Congratulations. Seems like we're all done for today!")
            current_time = int(self.utils.get_current_time())
            if current_time not in self.times:
                time.sleep(40)
                continue
            
            self.utils.speech.say_and_print(f"The time is {' '.join(self.utils.get_twelve_time(current_time))}. Your task is {self.tasks[current_time]}")
            time.sleep(40)
            self.utils.speech.say_and_print(f"The time is {' '.join(self.utils.get_twelve_time(current_time))}. Your task is {self.tasks[current_time]}")

            self.times.remove(current_time)