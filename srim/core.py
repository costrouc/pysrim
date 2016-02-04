""" Core components of SRIM simulation

"""

import os
import re
from math import sqrt

import yaml
import srim

from srim import units


class Element:
    """ Initialize elements from the periodic table

    """
    _db = None

    def __init__(self, symbol, mass=None):
        if Element._db is None:
            dbpath = os.path.join(srim.__path__[0], 'data', 'elements.yaml')
            Element._db = yaml.load(open(dbpath, "r"))

        element = self._lookup(symbol)
        self.atomic_number = element['z']
        self.symbol = element['symbol']
        self.name = element['name']

        if mass:
            self.mass = mass
        else:
            self.mass = element['mass']

    def _lookup(self, identifier):
        """ Looks up element from symbol, name, or atomic number

        :param str or int identifier: Unique symbol, name, or atomic number of element
        """
        if re.match("[A-Z][a-z]?", identifier): # Symbol
            return self._db.get(identifier)
        if re.match("[A-Z][a-z]*", identifier): # Name
            for symbol in self._db:
                if self._db[symbol]['name'] == identifier:
                    return self._db[symbol]
            raise KeyError('name:{} does not exist'.format(identifier))
        if isinstance(identifier, int): # Atomic Number
            for symbol in self._db:
                if self._db[symbol]['z'] == identifier:
                    return self._db[symbol]
            raise IndexError('z:{} does not exist'.format(identifier))
        else:
            raise NotImplementedError('identifier type:{} value:{} not recognized'.format(
                type(identifier), identifier))

    def __repr__(self):
        return "<Element symbol:{} name:{} mass:{:2.2f}>".format(
            self.symbol, self.name, self.mass)


class Material:
    """ Material Representation """
    def __init__(self, stoichiometry, density=None):
        """ Create Material from stoichiometry and density

        :param str or list stoichiometry: stoichiometry of material
        :param float density: Density [g/cm^3] of material

        Stoichiometry can be specified in many ways.
         - 'SiC'
         - 'CO2'
         - 'Cu99.0Ni1'
         - [['Cu', 99], ['Ni', 1.0]]
         - [[Element('Cu'), 99], [Element('Ni'), 1.0]]
        """
        elements = []

        if isinstance(stoichiometry, str):
            single_regex = '([A-Z][a-z]?)([0-9]*(?:\.[0-9]*))?'
            stoichiometry_regex = '(?:{})+'.format(single_regex)
            if re.match(stoichiometry_regex, stoichiometry):
                matches = re.findall(single_regex, stoichiometry)
                for match in matches:
                    symbol, fraction = match
                    if fraction == '':
                        match[1] = 1
                    elements.append(Element(symbol), float(fraction))
            else:
                raise ValueError('stoichiometry str {} unrecognized'.format(stoichiometry))
        elif isinstance(stoichiometry, list):
            for element, fraction in stoichiometry:
                if isinstance(element, Element):
                    elements.append(element, float(fraction))
                else:
                    elements.append(Element(element), float(fraction))
        else:
            raise NotImplementedError('stoichometry must be str or list see doc')



class Ion(Element):
    """ Ion traveling through medium

    """
    def __init__(self, symbol, energy, mass=None):
        """Initialize Ion

        :param int or str symbol: Atomic symbol of element
        :param float energy: Energy [eV] of ion
        :param float mass: Mass [amu] of ion
        """
        self.energy = energy
        super().__init__(symbol, mass)

    def __repr__(self):
        return "<Ion element:{} mass:{} energy:{} keV>".format(
            self.name, self.mass, self.energy)


    @property
    def velocity(self):
        """ Velocity of Ion [m/s] """
        return sqrt(2 * (self.energy * units.eV) / (self.mass * units.amu))


class Target:
    """ Target that Ion impacts

    """
    def __init__(self, layers):
        self.layers = layers


    @property
    def width(self):
        """ total width of target """
        return sum(layer.width for layer in self.layers)


class Layer(Material):
    """ Represents a layer in target

    """
    def __init__(self, material, width):
        self.width = width
        super().__init__(material)

    def __repr__(self):
        return "<Layer material:{} width:{}>".format(self.chemical_formula, self.width)

