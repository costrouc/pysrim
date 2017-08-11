""" Module for automating srim calculations

"""
import os
import subprocess
import shutil

from .core.utils import (
    check_input,
    is_zero, is_zero_or_one, is_zero_to_two, is_zero_to_five, is_one_to_seven, is_one_to_eight,
    is_srim_degrees,
    is_positive,
    is_quoteless
)

from .output import Results
from .input import AutoTRIM, TRIMInput, SRInput


SRIM_DIRECTORY = os.path.join(os.sep, 'tmp', 'srim')


class SRIMSettings(object):
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
        self.settings = SRIMSettings(**args)
        self.calculation = check_input(int, is_one_to_seven, calculation)
        self.number_ions = check_input(int, is_positive, number_ions)
        self.target = target
        self.ion = ion


    def _write_input_files(self):
        """ Write necissary TRIM input files for calculation """
        AutoTRIM().write()
        TRIMInput(self).write()

    @staticmethod
    def copy_output_files(src_directory, dest_directory, check_srim_output=True):
        known_files = {
            'TRIM.IN', 'PHONON.txt', 'E2RECOIL.txt', 'IONIZ.txt',
            'LATERAL.txt', 'NOVAC.txt', 'RANGE.txt', 'VACANCY.txt',
            'COLLISON.txt', 'BACKSCAT.txt', 'SPUTTER.txt',
            'RANGE_3D.txt', 'TRANSMIT.txt', 'TRIMOUT.txt'
        }

        if not os.path.isdir(src_directory):
            raise ValueError('src_directory must be path')

        if not os.path.isdir(dest_directory):
            raise ValueError('dest_directory must be path')

        for known_file in known_files:
            if os.path.isfile(os.path.join(
                    src_directory, known_file)):
                shutil.copy(os.path.join(
                    src_directory, known_file), dest_directory)
            elif os.path.isfile(os.path.join(src_directory, 'SRIM Outputs', known_file)) and check_srim_output:
                shutil.copy(os.path.join(
                    src_directory, 'SRIM Outputs', known_file), dest_directory)

    def run(self, srim_directory=SRIM_DIRECTORY):
        current_directory = os.getcwd()
        os.chdir(srim_directory)
        self._write_input_files()
        # Make sure compatible with Windows, OSX, and Linux
        subprocess.check_call(['wine', str(os.path.join('.', 'TRIM.exe'))])
        os.chdir(current_directory)

        return Results(srim_directory)


class SRSettings(object):
    """ SR Settings """
    def __init__(self, **args):
        self._settings = {
            'energy_min': check_input(float, is_positive, args.get('energy_min', 1.0E3)),
            'output_type': check_input(int, is_one_to_eight, args.get('output_type', 1)),
            'output_filename': args.get('output_filename', 'SR_OUTPUT.txt'),
            'correction': check_input(float, is_positive, args.get('correction', 1.0))
        }

    def __getattr__(self, attr):
        return self._settings[attr]


class SR(object):
    """ Automate SR Calculations """
    def __init__(self, layer, ion, **args):
        self.settings = SRSettings(**args)
        self.layer = layer
        self.ion = ion

    def  _write_input_file(self):
        """ Write necissary SR input file for calculation """
        SRInput(self).write()

    def run(self, srim_directory=SRIM_DIRECTORY):
        current_directory = os.getcwd()
        os.chdir(os.path.join(srim_directory, 'SR Module'))
        self._write_input_file()
        # Make sure compatible with Windows, OSX, and Linux
        subprocess.check_call([str(os.path.join('.', 'SRModule.exe'))])
        os.chdir(current_directory)
