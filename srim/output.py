""" Read output files of SRIM simulation

"""
import os
import re
from io import StringIO

import numpy as np

class Ioniz(object):
    def __init__(self, directory, filename='IONIZ.txt'):
        with open(os.path.join(directory, filename)) as f:
            output = f.read()
        
            # Data Location
            match = re.search('-----------  -----------  -----------', output)
            if match:
                data = np.loadtxt(StringIO(output[match.end():]))

class Range(object):
    """ Table of the final distribution of the ions, and any recoiling target atoms
    """
    pass

class Backscat(object):
    """ The kinetics of all backscattered ions (energy, location and trajectory)
    """
    pass

class Transmit(object):
    """ The kinetics of all transmitted ions (energy, location and trajectory)
    """
    pass

class Sputter(object):
    """ The kinetics of all target atoms sputtered from the target.
    """
    pass


