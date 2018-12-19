from klego import *

paramset_a = {
        'time': '12-19, about 16:30, ambient light level 250-310',
        'style': 'stable',
        'ambient light interval': (250, 310),
        'features enabled': None,
        'kp': 0.65,
        'ki': 0.02,
        'kd': 0.03,
        'offset': 275,
        'tp': 85,
        'reflexive_light': 0  # disabled
    }

paramset_b = {
    'time': '12-19, about 17:20',
    'style': 'violent',
    'ambient light interval': None
}

paramset_redirect = {
    'stable_twilight': paramset_a,
    'vialent_twilight': paramset_b
}

def run(mode):
    """
    todo： select or create one param set
    """
    parameters = {
        'kp': 0,
        'ki': 0,
        'kd': 0,
        'offset': 0,
        'tp': 0
    }
    pid.kp = parameters['kp']
    pid.ki = parameters['ki']
    pid.kd = parameters['kd']
    pid.tp = parameters['tp']
    pid.offset = parameters['offset']

    pid.when("encountered_cross()", "")
    pid.when("brightness() > 342", "None")
    pid.run()
