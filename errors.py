"""A file where I have custom errors. Just something about having Custom Errors makes me feel satisfied."""

class NonExistentDay(ValueError):
    """Error raised when no valid day could be found for a given input!"""

    def __init__(self, day:str, extra:str=""):

        message = f"NonExistentDayError: No day beginning with {day} exists as far as I know. {extra}"

        super().__init__(message)

class BadDayInformation(ValueError):
    """Exception raised when a day file's information is not formatted correctly."""

    def __init__(self, line:str, filename:str, extra:str=""):

        message = f"BadDayInformation: The information provided in the file {filename} was badly formatted. Format should be: time_in_24hourclock: task.\nLine: {line}.\nExtra: {extra}"

        super().__init__(message)
