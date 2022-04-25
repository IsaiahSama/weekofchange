import sys
from time import sleep

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
        utils (Utils): An instance of the Utils class
        schedule (Schedule): An instance of the Schedule class
    Methods:
        main(): The main method of the Program.
        """

    def __init__(self) -> None:
        self.utils = None
        self.schedule = None

    def main(self):
        """The main method of the program. Controls the main flow!"""
        self.utils = mechanics.Utils()
        self.utils.setup()
        self.schedule = mechanics.Schedule(self.utils)
        self.schedule.load_schedule()
        try:
            self.schedule.start_threads()
        except KeyboardInterrupt:
            raise
        except Exception as err:
            print(err)
            raise
        
        # recog = mechanics.SpeechRecog()

        while True:
            # try:
            #     spoken = recog.listen()
            # except sr.RequestError as err:
            #     print("An error has occurred", err)
            # except KeyboardInterrupt:
            #     raise SystemExit
            # except:
            #     continue
            
            # if spoken.lower() == "schedule":
            #     try:
            #         recog.listen()
            #     except sr.UnknownValueError:
            #         self.utils.speech.say("Apologies. I have no idea what you asked!")
            #     except sr.RequestError as err:
            #         self.utils.speech.say("Apologies. Seems there is a request error. I have sent it to the screen for your viewing.")
            #         print(err)

            sleep(5)


if __name__ == "__main__":
    main = Main()
    main.main()
