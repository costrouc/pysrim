""" Module for automating srim calculations

"""
import os
import subprocess

from .core.utils import (
    check_input,
    is_zero, is_zero_or_one, is_zero_to_two, is_zero_to_five, is_one_to_seven,
    is_srim_degrees,
    is_positive,
    is_quoteless
)

from .input import AutoTRIM, TRIMInput
 

SRIM_DIRECTORY = os.path.join('/tmp', 'srim')


class Settings(object):
    """ SRIM Settings 

    TODO: Readonly becuase I have not constructed getter and setters
    """
    def __init__(self, **args):
        self._settings = {
            'description': check_input(str, is_quoteless, args.get('description', 'srim-python run')),
            'reminders': check_input(int, is_zero_or_one, args.get('reminders', 0)),
            'autosave': check_input(int, is_zero_or_one, args.get('autosave', 0)),
            'plot_mode': check_input(int, is_zero_to_five, args.get('plot_mode', 5)),
            'plot_xmin': check_input(float, is_positive, args.get('plot_xmin', 0.0)),
            'plot_xmax': check_input(float, is_positive, args.get('plot_xmax', 0.0)), 
            'ranges': check_input(int, is_zero_or_one, args.get('ranges', 0)),
            'backscattered': check_input(int, is_zero_or_one, args.get('backscattered', 0)),
            'transmit': check_input(int, is_zero_or_one, args.get('transmit', 0)),
            'sputtered': check_input(int, is_zero_or_one, args.get('ranges', 0)),
            'collisions': check_input(int, is_zero_to_two, args.get('collisions', 0)),
            'exyz': check_input(int, is_zero_or_one, args.get('exyz', 0)),
            'angle_ions': check_input(float, is_srim_degrees, args.get('angle_ions', 0.0)),
            'bragg_correction': float(args.get('bragg_correction', 1.0)), # TODO: Not sure what correct values are
            'random_seed': check_input(int, is_positive, args.get('random_seed', 0)),
            'version': check_input(int, is_zero_or_one, args.get('version', 0)),
        }

        if self.plot_xmin > self.plot_xmax:
            raise ValueError('xmin must be <= xmax')

    def __getattr__(self, attr):
        return self._settings[attr]


class SRIM(object):
    """ Automate SRIM Calculations

    """
    def __init__(self, target, ion, calculation=1, number_ions=1000, **args):
        """ Initialize srim object with settings 

        TODO: fill out doc strings
        """
        self.settings = Settings(**args)
        self.calculation = check_input(int, is_one_to_seven, calculation)
        self.number_ions = check_input(int, is_positive, number_ions)
        self.target = target
        self.ion = ion


    def _write_input_files(self):
        """ Write necissary TRIM input files for calculation """

        AutoTRIM().write()
        TRIMInput(self).write()

    def _copy_output_files(self):
        pass

    def run(self):
        os.chdir(SRIM_DIRECTORY)
        
        self._write_input_files()
        subprocess.check_call(['./TRIM.exe'])
        self._copy_output_files()

