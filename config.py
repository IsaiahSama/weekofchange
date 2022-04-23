import yaml 
from os.path import exists

default = {
    "folder_location": "./schedules/",
    "text_to_speech": {'rate': 200, 'volume': 1.0, 'voice': 1} 
}

def load_yaml() -> dict:
    """Function used to load in yaml, and return the result"""
    if not exists("config.yaml"):
        print("Configuration file is missing. Using defaults.")
        return default
    
    with open("config.yaml", "r") as fp:
        config = yaml.safe_load(fp)

    for key in default.keys():
        if key not in config:
            config[key] = default[key]

    return config