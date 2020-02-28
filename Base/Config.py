import re
class ConfigClass:
    size = width, height = 640, 800
    fps = 60
    max_life = 3000
    game_ctr = 3
    key_guns_ctr =1 
    auto_guns_ctr =9 
    def __init__(self):
        pass

    def __setitem__(self, name, value):
        setattr(ConfigClass, name, value)

    def __getitem__(self, name):
        return getattr(ConfigClass, name)

def get_val(name):
    return getattr(ConfigClass, name)
def set_val(name, value):
    return setattr(ConfigClass, name, value)

config = None

def init():
    global config
    config = ConfigClass()
