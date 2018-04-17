""" Read output files of SRIM simulation

TODO: Read header information
"""
import os
import re
from io import BytesIO

import numpy as np

from .core.ion import Ion

# Valid double_regex 4, 4.0, 4.0e100
double_regex = r'[-+]?\d+\.?\d*(?:[eE][-+]?\d+)?'
symbol_regex = r'[A-Z][a-z]?'
int_regex = '[+-]?\d+'


class SRIMOutputParseError(Exception):
    """SRIM error reading output file"""
    pass


class SRIM_Output(object):
    def _read_name(self, output):
        raise NotImplementedError()

    def _read_ion(self, output):
        ion_regex = 'Ion\s+=\s+({})\s+Energy\s+=\s+({})\s+keV'.format(
            symbol_regex, double_regex)
        match = re.search(ion_regex.encode('utf-8'), output)
        if match:
            symbol = str(match.group(1).decode('utf-8'))
            energy = float(match.group(2)) #keV
            return Ion(symbol, 1000.0 * energy)
        raise SRIMOutputParseError("unable to extract ion from file")

    def _read_target(self, output):
        match_target = re.search(b'(?<=====\r\n)Layer\s+\d+\s+:.*?(?=====)', output, re.DOTALL)
        if match_target:
            print(match_target.group(0))
            layer_regex = (
                'Layer\s+(?P<i>\d+)\s+:\s+(.+)\r\n'
                'Layer Width\s+=\s+({0})\s+A\s+;\r\n'
                '\s+Layer #\s+(?P=i)- Density = ({0}) atoms/cm3 = ({0}) g/cm3\r\n'
                '((?:\s+Layer #\s+(?P=i)-\s+{1}\s+=\s+{0}\s+Atomic Percent = {0}\s+Mass Percent\r\n)+)'
            ).format(double_regex, symbol_regex)
            layers = re.findall(layer_regex.encode('utf-8'), match_target.group(0))
            if layers:
                element_regex = (
                    '\s+Layer #\s+(\d+)-\s+({1})\s+=\s+({0})\s+Atomic Percent = ({0})\s+Mass Percent\r\n'
                ).format(double_regex, symbol_regex)
                element_regex = element_regex.encode()

                layers_elements = []
                for layer in layers:
                    # We know that elements will match
                    layers_elements.append(re.findall(element_regex, layer[5]))

                raise NotImpementedError()

                import pytest
                pytest.set_trace()

        raise SRIMOutputParseError("unable to extract total target from file")

    def _read_num_ions(self, output):
        match = re.search(b'Total Ions calculated\s+=(\d+.\d+)', output)
        if match:
            # Cast string -> float -> round down to nearest int
            return int(float(match.group(1)))
        raise SRIMOutputParseError("unable to extract total ions from file")

    def _read_table(self, output):
        match = re.search((
            b'=+(.*)'
            b'-+(?:\s+-+)+'
        ), output, re.DOTALL)
        # Read Data from table

        if match:
            # Headers TODO: name the columns in table
            header = None

            # Data
            data = np.genfromtxt(BytesIO(output[match.end():]), max_rows=100)
            return data
        raise SRIMOutputParseError("unable to extract table from file")


class Results(object):
    """ Gathers all results from folder

    Parameters
    ----------
    directory : :obj:`str`
        directory to look for TRIM calculations

    Notes
    -----
    Files that are looked for:
      - ``IONIZ.txt`` handled by :class:`srim.output.Ioniz`
      - ``VACANCY.txt`` handled by :class:`srim.output.Vacancy`
      - ``NOVAC.txt`` handled by :class:`srim.output.NoVacancy`
      - ``E2RECOIL.txt`` handled by :class:`srim.output.EnergyToRecoils`
      - ``PHONON.txt`` handled by :class:`srim.output.Phonons`
      - ``RANGE.txt`` handled by :class:`srim.output.Range`
    """
    def __init__(self, directory):
        """ Retrives all the calculation files in a given directory"""
        self.ioniz = Ioniz(directory)
        self.vacancy = Vacancy(directory)

        try:
            self.novac = NoVacancy(directory)
        except ValueError:
            self.novac = None

        self.etorecoils = EnergyToRecoils(directory)
        self.phonons = Phonons(directory)
        self.range = Range(directory)


class Ioniz(SRIM_Output):
    """``IONIZ.txt`` Ionization by ions and depth. Includes header information about calculation

    Parameters
    ----------
    directory : :obj:`str`
         directory of calculation
    filename : :obj:`str`, optional
         filename for Ioniz. Default ``IONIZ.txt``
    """
    def __init__(self, directory, filename='IONIZ.txt'):
        with open(os.path.join(directory, filename), 'rb') as f:
            output = f.read()
            ion = self._read_ion(output)
            num_ions = self._read_num_ions(output)
            data = self._read_table(output)

        self._ion = ion
        self._num_ions = num_ions
        self._depth = data[:, 0]
        self._ions = data[:, 1]
        self._recoils = data[:, 2]

    @property
    def ion(self):
        """ Ion used in SRIM calculation

        **mass** could be wrong
        """
        return self._ion

    @property
    def num_ions(self):
        """ Number of Ions in SRIM simulation """
        return self._num_ions

    @property
    def depth(self):
        """ Depth [Ang] of bins in SRIM Calculation """
        return self._depth

    @property
    def ions(self):
        """Ionization energy [eV/(Angstrom Ion)] lost to electronic stopping
        in incident ions"""
        return self._ions

    @property
    def recoils(self):
        """Ionization energy [eV/(Angstrom Ion)] lost to electronic stopping
        in recoil ions"""
        return self._recoils


class Vacancy(SRIM_Output):
    """``VACANCY.txt`` Table of the final distribution of vacancies vs depth

    Parameters
    ----------
    directory : :obj:`str`
         directory of calculation
    filename : :obj:`str`, optional
         filename for Vacancy. Default ``VACANCY.txt``
    """
    def __init__(self, directory, filename='VACANCY.txt'):
        with open(os.path.join(directory, filename), 'rb') as f:
            output = f.read()
            ion = self._read_ion(output)
            num_ions = self._read_num_ions(output)
            data = self._read_table(output)

        self._ion = ion
        self._num_ions = num_ions
        self._depth = data[:, 0]
        self._ion_knock_ons = data[:, 1]
        self._vacancies = data[:, 2:]

    @property
    def ion(self):
        """ Ion used in SRIM calculation

        **mass** could be wrong
        """
        return self._ion

    @property
    def num_ions(self):
        """Number of Ions in SRIM simulation"""
        return self._num_ions

    @property
    def depth(self):
        """Depth [Ang] of bins in SRIM Calculation"""
        return self._depth

    @property
    def knock_ons(self):
        """Vacancies produced [Vacancies/(Angstrom-Ion) by ion]"""
        return self._ion_knock_ons

    @property
    def vacancies(self):
        """Vacancies [Vacancies/(Angstrom-Ion)] produced of element in layer"""
        return self._vacancies


class NoVacancy(SRIM_Output):
    """ ``NOVAC.txt`` Table of Replacement Collisions

    Parameters
    ----------
    directory : :obj:`str`
         directory of calculation
    filename : :obj:`str`, optional
         filename for NoVacancy. Default ``NOVAC.txt``
    """
    def __init__(self, directory, filename='NOVAC.txt'):
        with open(os.path.join(directory, filename), 'rb') as f:
            output = f.read()

            # Check if it is KP calculation
            if re.search(b'Recoil/Damage Calculations made with Kinchin-Pease Estimates',
                         output):
                raise ValueError('NOVAC has no data for KP calculations')

            ion = self._read_ion(output)
            num_ions = self._read_num_ions(output)
            data = self._read_table(output)

        self._ion = ion
        self._num_ions = num_ions
        self._depth = data[:, 0]
        self._number = data[:, 1]

    @property
    def ion(self):
        """ Ion used in SRIM calculation

        **mass** could be wrong
        """
        return self._ion

    @property
    def num_ions(self):
        """Number of Ions in SRIM simulation"""
        return self._num_ions

    @property
    def depth(self):
        """Depth [Ang] of bins in SRIM Calculation"""
        return self._depth

    @property
    def number(self):
        """Replacement Collisions [Number/(Angstrom-Ion)]"""
        return self._number


class EnergyToRecoils(SRIM_Output):
    """``E2RECOIL.txt`` Energy transfered to atoms through binary collision

    Parameters
    ----------
    directory : :obj:`str`
         directory of calculation
    filename : :obj:`str`, optional
         filename for EnergyToRecoils. Default ``E2RECOIL.txt``
    """
    def __init__(self, directory, filename='E2RECOIL.txt'):
        with open(os.path.join(directory, filename), 'rb') as f:
            output = f.read()
            ion = self._read_ion(output)
            num_ions = self._read_num_ions(output)
            data = self._read_table(output)

        self._ion = ion
        self._num_ions = num_ions
        self._depth = data[:, 0]
        self._ions = data[:, 1]
        self._recoils = data[:, 2:]

    @property
    def ion(self):
        """Ion used in SRIM calculation

        **mass** could be wrong
        """
        return self._ion

    @property
    def num_ions(self):
        """Number of Ions in SRIM simulation"""
        return self._num_ions

    @property
    def depth(self):
        """Depth [Ang] of bins in SRIM Calculation"""
        return self._depth

    @property
    def ions(self):
        """Energy [eV/(Angstrom-Ion)] transfered to material through ion collisions"""
        return self._ions

    @property
    def absorbed(self):
        """Energy [eV/(Angstrom-Ion)] absorbed from collisions with Atom

        TODO: fix terminology
        """
        return self._recoils


class Phonons(SRIM_Output):
    """``PHONON.txt``  Distribution of Phonons

    Parameters
    ----------
    directory : :obj:`str`
         directory of calculation
    filename : :obj:`str`, optional
         filename for Phonons. Default ``PHONON.txt``
    """
    def __init__(self, directory, filename='PHONON.txt'):
        with open(os.path.join(directory, filename), 'rb') as f:
            output = f.read()
            ion = self._read_ion(output)
            num_ions = self._read_num_ions(output)
            data = self._read_table(output)

        self._ion = ion
        self._num_ions = num_ions
        self._depth = data[:, 0]
        self._ions = data[:, 1]
        self._recoils = data[:, 2]

    @property
    def ion(self):
        """Ion used in SRIM calculation

        **mass** could be wrong
        """
        return self._ion

    @property
    def num_ions(self):
        """Number of Ions in SRIM simulation"""
        return self._num_ions

    @property
    def depth(self):
        """Depth [Ang] of bins in SRIM Calculation"""
        return self._depth

    @property
    def ions(self):
        """Number of phonons [Phonons/(Angstrom Ion)] created from ions collisions"""
        return self._ions

    @property
    def recoils(self):
        """Number of phonons [Phonons/(Angstrom Ion)] created from recoils
        resulting from ion collisions"""
        return self._recoils


class Range(SRIM_Output):
    """``RANGE.txt`` Table of the final distribution of the ions, and any recoiling target atoms

    Parameters
    ----------
    directory : :obj:`str`
         directory of calculation
    filename : :obj:`str`, optional
         filename for Range. Default ``RANGE.txt``
    """
    def __init__(self, directory, filename='RANGE.txt'):
        with open(os.path.join(directory, filename), 'rb') as f:
            output = f.read()
            ion = self._read_ion(output)
            num_ions = self._read_num_ions(output)
            data = self._read_table(output)

        self._ion = ion
        self._num_ions = num_ions
        self._depth = data[:, 0]
        self._ions = data[:, 1]
        self._elements = data[:, 2:]

    @property
    def ion(self):
        """Ion used in SRIM calculation

        **mass** could be wrong
        """
        return self._ion

    @property
    def num_ions(self):
        """Number of Ions in SRIM simulation"""
        return self._num_ions

    @property
    def depth(self):
        """Depth [Ang] of bins in SRIM Calculation"""
        return self._depth

    @property
    def ions(self):
        """Ion final distribution [(Atoms/cm3)/(Atoms/cm2)]"""
        return self._ions

    @property
    def elements(self):
        """Per elements [(Atoms/cm3)/(Atoms/cm2)] distribution of each element"""
        return self._elements



class Backscat(object):
    """ The kinetics of all backscattered ions (energy, location and trajectory)

    TODO: one day to be implemented! submit pull request please!
    """
    pass


class Transmit(object):
    """ The kinetics of all transmitted ions (energy, location and trajectory)

    TODO: one day to be implemented! submit pull request please!
    """
    pass


class Sputter(object):
    """ The kinetics of all target atoms sputtered from the target.

    TODO: one day to be implemented! submit pull request please!
    """
    pass


class Collision:
    """Reads the SRIM Collisions file.

    This is the most important file in my opinion. It records every
    single collision and its energies. The file will get huge for
    simulations with many collisions. Since the file can be larger
    than the amount of RAM it will read the file in sections
    (buffers).

    Parameters
    ----------
    directory : :obj:`str`
         directory of calculation
    filename : :obj:`str`, optional
         filename for Collisions. Default ``COLLISON.txt``

    """
    def __init__(self, directory, filename='COLLISON.txt'):
        self.filename = os.path.join(directory, filename)

        with open(filename, encoding="latin-1") as f:
            self._read_header(f)

        self._ion_index = buffered_findall(filename, b"  Ion    Energy")

    def _read_header(self, f):
        """Read Header of COLLISON.txt

        Currently we do nothing with the header
        """

        # Collect the header of the file
        header = []

        for line in f:
            if line == " \n":
                break
            header.append(line)
        return header

    def _read_ion(self, ion_str):
        """There are 2 types of files with and without cascades

        format:
           1 - Kinchin-Pease Theory (No full cascades)
           2 - full cascades
        """
        # Notice that lines is an generator!
        # This makes it so we can walk through lines
        # in multiple for loops
        lines = (line for line in ion_str.split('\n'))

        # Skip Ion Header
        for line in lines:
            if re.match("^-+\r$", line):
                break

        collisions = []

        # Reads collisions for an ion
        for line in lines:
            if re.match("^=+\r$", line):
                break

            tokens = line.split(chr(179))[1:-1]

            # Check if a full_cascades simulation
            # Read Cascade information
            if re.match(r"\s+<== Start of New Cascade\s+", tokens[-1]):
                (target_disp,
                 target_vac,
                 target_replac,
                 target_inter,
                 cascade) = self._read_cascade(lines)
            else:
                target_disp = float(tokens[8])
                target_vac = 0
                target_replac = 0
                target_inter = 0
                cascade = None

            collisions.append({
                'ion_number': int(tokens[0]),
                'kinetic_energy': float(tokens[1]),
                'depth': float(tokens[2]),
                'lat_y_dist': float(tokens[3]),
                'lat_z_dist': float(tokens[4]),
                'stopping_energy': float(tokens[5]),
                'atom': re.search("([A-Z][a-z]?)", tokens[6]).group(1),
                'recoil_energy': float(tokens[7]),
                'target_disp': target_disp,
                'target_vac': target_vac,
                'target_replac': target_replac,
                'target_inter': target_inter,
                'cascade': cascade
            })

            # Handles weird case where no summary of cascade
            if target_disp is None:
                break;

        # Reads ion footer
        ion_number = re.search(int_regex, next(lines)).group(0)

        footer = ""
        for line in lines:
            if re.match("^=+\r$", line):
                break
            footer += line

        matches = re.findall(double_regex, footer)

        line = next(lines)

        return {
            'ion_number': int(ion_number),
            'displacements': float(matches[0]),
            'avg_displacements': float(matches[1]),
            'replacements': float(matches[2]),
            'avg_replacements': float(matches[3]),
            'vacancies': float(matches[4]),
            'avg_vacancies': float(matches[5]),
            'interstitials': float(matches[6]),
            'avg_interstitials': float(matches[7]),
            'sputtered_atoms': float(matches[8]),
            'avg_sputtered_atoms': float(matches[9]),
            'transmitted_atoms': float(matches[10]),
            'avg_transmitted_atoms': float(matches[11]),
            'collisions': collisions
        }

    def _read_cascade(self, lines):
        line = next(lines)

        assert re.match("^=+\r$", line)


        line = next(lines)
        assert re.match((
                "  Recoil Atom Energy\(eV\)   X \(A\)      Y \(A\)      Z \(A\)"
                "   Vac Repl Ion Numb \d+="
        ), line)

        cascade = []
        for line in lines:
            if re.match("^=+\r$", line):
                break
            tokens = line.split()[1:-1]

            print(tokens)
            cascade.append({
                'recoil': int(tokens[0]),
                'atom': int(tokens[1]),
                'recoil_energy': float(tokens[2]),
                'position': np.array([float(tokens[3]),
                                      float(tokens[4]),
                                      float(tokens[5])]),
                'vac': int(tokens[6]),
                'repl': int(tokens[7])
            })

        if line.count('=') > 100:
            return None, None, None, None, cascade

        line = next(lines)
        tokens = line.split(chr(179))[1:-1]

        if tokens:

            target_disp = float(tokens[2])
            target_vac = float(tokens[3])
            target_replac = float(tokens[4])
            target_inter = float(tokens[5])
        else:
            target_disp = None
            target_vac = None
            target_replac = None
            target_inter = None

        return target_disp, target_vac, target_replac, target_inter, cascade

    def __getitem__(self, i):
        start = self._ion_index[i]

        if i == len(self._ion_index):
            end = os.path.getsize(self.filename)
        else:
            end = self._ion_index[i+1]

        with open(self.filename, "rb") as f:
            f.seek(start)
            # We assume that ion_str will fit in RAM
            ion_str = f.read(end - start)
            return self._read_ion(ion_str.decode('latin-1'))

    def __len__(self):
        return len(self._ion_index) - 1


def buffered_findall(filename, string, start=0):
    """A method of reading a file in buffered pieces (needed for HUGE files)"""
    with open(filename, 'rb') as f:
        filesize = os.path.getsize(filename)
        BUFFERSIZE = 4096
        overlap = len(string) - 1
        buffer = None
        positions = []

        if start > 0:
            f.seek(start)

        while True:
            if (f.tell() >= overlap and f.tell() < filesize):
                f.seek(f.tell() - overlap)
            buffer = f.read(BUFFERSIZE)
            if buffer:
                buffer_positions = [m.start() for m in re.finditer(string, buffer)]

                for position in buffer_positions:
                    if position >= 0:
                        positions.append(f.tell() - len(buffer) + position)
            else:
                return positions
