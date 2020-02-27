class vars:
    size = width, height = 640, 800
    fps = 60
    max_life = 500
    game_ctr = 3

def set_val(name, val):
    setattr(vars, name, val)

def get_val(name):
    if hasattr(vars, name):
        return getattr(vars, name)
