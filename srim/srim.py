""" Module for automating srim calculations

"""
import os
import random
import subprocess
import shutil
import distutils.spawn

from .core.utils import (
    check_input,
    is_zero, is_zero_or_one, is_zero_to_two, is_zero_to_five,
    is_one_to_seven, is_one_to_eight,
    is_srim_degrees,
    is_positive,
    is_quoteless
)

from .output import Results, SRResults
from .input import AutoTRIM, TRIMInput, SRInput
from .config import DEFAULT_SRIM_DIRECTORY


class TRIMSettings(object):
    """ TRIM Settings

    This object can construct all options available when running a TRIM calculation.

    Parameters
    ----------
    description : :obj:`str`, optional
       A name to give calculation. Has no effect on the actual
       calculation.
    reminders : :obj:`str`, optional
       TODO: could not find description. default 0
    autosave : :obj:`int`, optional
       save calculations after every `autosave` steps. default 0 will
       not autosave except at end
    plot_mode : :obj:`int`, optional
       Default 5.
       (0) ion distribution with recoils projected on y-plane
       (1) ion distribution with recoils projected on z-plane
       (2) ion distribution without recoils projected on y-plane
       (3) transverse plot of ions + recoil cascades, yz-plane
       (4) all four (0-3) on one screen
       (5) no graphics (default and at least 5X faster than others)
    plot_xmin : :obj:`float`, optional
       minimum x depth to plot only really matters if ``plot_mode``
       between 0-4. Default 0.0.
    plot_xmax : :obj:`float`, optional
       maximum x depth to plot only really matters if ``plot_mode``
       between 0-4. Default 0.0.
    ranges : :obj:`bool`, optional
       whether include ``RANGES.txt``, ``RANGE_3D.txt`` to output
       files. Default (0) False
    backscattered : :obj:`bool`, optional
       whether include ``BACKSCAT.txt`` to output files. Default (0)
       False
    transmit : :obj:`bool`, optional
       whether include ``TRANSMIT.txt`` to output files. Default (0)
       False
    sputtered : :obj:`bool`, optional
       whether include ``SPUTTER.txt`` to output files. Default (0)
       False
    collisions : :obj:`bool`, optional
       whether include ``COLLISON.txt`` to output files. Yes they did
       mispell collisions. Default (0) False
    exyz : int
       increment in eV to use for ``EXYZ.txt`` file. Default (0)
    angle_ions : :obj:`float`, optional
       angle of incidence of the ion with respect to the target
       surface. Default (0) perpendicular to the target surface along
       x-axis. Values 0 - 89.9.
    bragg_correction : :obj:`float`, optional
       bragg correction to stopping. Default (0) no correction
    random_seed : :obj:`int`, optional
       a random seed to start calculation with. Default random integer
       between 0 and 100,000. Thus all calculations by default are random.
    version : :obj:`int`, optional
       SRIM-2008 or SRIM-2008 so not really much choice. Default (0)

    Notes
    -----
        This class should never explicitely created. Instead set as
        kwargs in :class:`srim.srim.TRIM`
    """
    def __init__(self, **kwargs):
        """Initialize settings for a TRIM running"""
        self._settings = {
            'description': check_input(str, is_quoteless, kwargs.get('description', 'pysrim run')),
            'reminders': check_input(int, is_zero_or_one, kwargs.get('reminders', 0)),
            'autosave': check_input(int, is_zero_or_one, kwargs.get('autosave', 0)),
            'plot_mode': check_input(int, is_zero_to_five, kwargs.get('plot_mode', 5)),
            'plot_xmin': check_input(float, is_positive, kwargs.get('plot_xmin', 0.0)),
            'plot_xmax': check_input(float, is_positive, kwargs.get('plot_xmax', 0.0)),
            'ranges': check_input(int, is_zero_or_one, kwargs.get('ranges', 0)),
            'backscattered': check_input(int, is_zero_or_one, kwargs.get('backscattered', 0)),
            'transmit': check_input(int, is_zero_or_one, kwargs.get('transmit', 0)),
            'sputtered': check_input(int, is_zero_or_one, kwargs.get('ranges', 0)),
            'collisions': check_input(int, is_zero_to_two, kwargs.get('collisions', 0)),
            'exyz': check_input(int, is_positive, kwargs.get('exyz', 0)),
            'angle_ions': check_input(float, is_srim_degrees, kwargs.get('angle_ions', 0.0)),
            'bragg_correction': float(kwargs.get('bragg_correction', 1.0)), # TODO: Not sure what correct values are
            'random_seed': check_input(int, is_positive, kwargs.get('random_seed', random.randint(0, 100000))),
            'version': check_input(int, is_zero_or_one, kwargs.get('version', 0)),
        }

        if self.plot_xmin > self.plot_xmax:
            raise ValueError('xmin must be <= xmax')

    def __getattr__(self, attr):
        return self._settings[attr]


class TRIM(object):
    """ Automate TRIM Calculations

    Parameters
    ----------
    target : :class:`srim.core.target.Target`
        constructed target for TRIM calculation
    ion : :class:`srim.core.ion.Ion`
        constructed ion for TRIM calculation
    calculation : :obj:`int`, optional
        Default 1 quick KP calculation
        (1) Ion Distribution and Quick Calculation of Damage (quick KP)
        (2) Detailed Calculation with full Damage Cascades (full cascades)
        (3) Monolayer Collision Steps / Surface Sputtering
        (4) Ions with specific energy/angle/depth (quick KP damage) using TRIM.DAT
        (5) Ions with specific energy/angle/depth (full cascades) using TRIM.DAT
        (6) Recoil cascades from neutrons, etc. (full cascades) using TRIM.DAT
        (7) Recoil cascades and monolayer steps (full cascades) using TRIM.DAT
        (8) Recoil cascades from neutrons, etc. (quick KP damage) using TRIM.DAT
    number_ions : :obj:`int`, optional
        number of ions that you want to simulate. Default 1000. A lot
        better than the 99999 default in TRIM...
    kwargs :
        See :class:`srim.srim.TRIMSettings` for available TRIM
        options. There are many and none are required defaults are
        appropriate for most cases.

    Notes
    -----
        If you are doing a simulation with over 1,000 ions it is
        recomended to split the calculaion into several smaller
        calculations. TRIM has been known to unexpectedly crash mainly
        due to memory usage.
    """
    def __init__(self, target, ion, calculation=1, number_ions=1000, **kwargs):
        """ Initialize TRIM calcualtion"""
        self.settings = TRIMSettings(**kwargs)
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
        """Copies known TRIM files in directory to destination directory

        Parameters
        ----------
        src_directory : :obj:`str`
            source directory to look for TRIM output files
        dest_directory : :obj:`str`
            destination directory to copy TRIM output files to
        check_srim_output : :obj:`bool`, optional
            ensure that all files exist
        """
        known_files = {
            'TRIM.IN', 'PHONON.txt', 'E2RECOIL.txt', 'IONIZ.txt',
            'LATERAL.txt', 'NOVAC.txt', 'RANGE.txt', 'VACANCY.txt',
            'COLLISON.txt', 'BACKSCAT.txt', 'SPUTTER.txt',
            'RANGE_3D.txt', 'TRANSMIT.txt', 'TRIMOUT.txt',
            'TDATA.txt'
        }

        if not os.path.isdir(src_directory):
            raise ValueError('src_directory must be directory')

        if not os.path.isdir(dest_directory):
            raise ValueError('dest_directory must be directory')

        for known_file in known_files:
            if os.path.isfile(os.path.join(
                    src_directory, known_file)):
                shutil.copy(os.path.join(
                    src_directory, known_file), dest_directory)
            elif os.path.isfile(os.path.join(src_directory, 'SRIM Outputs', known_file)) and check_srim_output:
                shutil.move(os.path.join(
                    src_directory, 'SRIM Outputs', known_file), dest_directory)

    def run(self, srim_directory=DEFAULT_SRIM_DIRECTORY):
        """Run configured srim calculation

        This method:
         - writes the input file to ``<srim_directory>/TRIM.IN``
         - launches ``<srim_directory>/TRIM.exe``. Uses ``wine`` if available (needed for linux and osx)

        Parameters
        ----------
        srim_directory : :obj:`str`, optional
            path to srim directory. ``SRIM.exe`` should be located in
            this directory. Default ``/tmp/srim/`` will absolutely
            need to change for windows.
        """
        current_directory = os.getcwd()
        try:
            os.chdir(srim_directory)
            self._write_input_files()
            # Make sure compatible with Windows, OSX, and Linux
            # If 'wine' command exists use it to launch TRIM
            if distutils.spawn.find_executable("wine"):
                subprocess.check_call(['wine', str(os.path.join('.', 'TRIM.exe'))])
            else:
                subprocess.check_call([str(os.path.join('.', 'TRIM.exe'))])
            os.chdir(current_directory)
            return Results(srim_directory)
        finally:
            os.chdir(current_directory)


class SRSettings(object):
    """ SR Settings

    Parameters
    ----------
    energy_min : :obj:`float`, optional
       lowest energy in [eV] to calculation range
    output_type : :obj:`int`, optional
       specify units for output table
       (1) eV/Angstrom
       (2) keV/micron
       (3) MeV/mm
       (4) keV / (ug/cm2)
       (5) MeV / (mg/cm2)
       (6) keV / (mg/cm2)
       (7) eV / (1E15 atoms/cm2)
       (8) L.S.S reduced units
    output_filename : :obj:`str`, optional
       filename to give for SR output from calcualtion
    correction : :obj:`float`, optional
       Bragg rule correction. Usually no correction needed for heavy
       elements. Default 1.0 implies 100% of value (no change). 1.1
       will increase by 10%.

    Notes
    -----
        This class should never explicitely created. Instead set as
        kwargs in :class:`srim.srim.SR`
    """
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
    """ Automate SR Calculations

    Parameters
    ----------
    leyer : :class:`srim.core.layer.Layer`
        constructed layer for SR calculation
    ion : :class:`srim.core.ion.Ion`
        constructed ion for SR calculation
    kwargs :
        See :class:`srim.srim.SRSettings` for available SR
        options. There are a few and none are required. Defaults are
        appropriate for most cases.
    """
    def __init__(self, layer, ion, **kwargs):
        self.settings = SRSettings(**kwargs)
        self.layer = layer
        self.ion = ion

    def _write_input_file(self):
        """ Write necissary SR input file for calculation """
        SRInput(self).write()

    def run(self, srim_directory=DEFAULT_SRIM_DIRECTORY):
        """Run configured srim calculation

        This method:
         - writes the input file to ``<srim_directory/SR Module/TRIM.IN``
         - launches ``<srim_directory>/SR Module/SRModule.exe``. Uses ``wine`` if available (needed for linux and osx)

        Parameters
        ----------
        srim_directory : :obj:`str`, optional
            path to srim directory. ``SRIM.exe`` should be located in
            this directory. Default ``/tmp/srim`` will absolutely need
            to be changed for windows.
        """
        current_directory = os.getcwd()
        try:
            os.chdir(os.path.join(srim_directory, 'SR Module'))
            self._write_input_file()
            # Make sure compatible with Windows, OSX, and Linux
            # If 'wine' command exists use it to launch TRIM
            if distutils.spawn.find_executable("wine"):
                subprocess.check_call(['wine', str(os.path.join('.', 'SRModule.exe'))])
            else:
                subprocess.check_call([str(os.path.join('.', 'SRModule.exe'))])

            return SRResults(os.path.join(srim_directory, 'SR Module'))
        finally:
            os.chdir(current_directory)
