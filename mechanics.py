"""File responsible for most of the mechanics that will be used throughout this program."""

from dataclasses import dataclass, field
import os
import pyttsx3

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
            day_file = os.path.join(Constants.folder_path, day + ".txt")
            if os.path.exists(day_file): continue
            with open(day_file, "w") as fp:
                fp.write(f"# {day}'s schedule goes here. Format: time_in_24_hours:task")

        self.speech.say_and_print("Everything has been setup correctly!!")

class Speech:
    """Class responsible for the setup and handling of the Text To Speech
    
    Attrs:
        
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

