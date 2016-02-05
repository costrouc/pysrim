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

        self._element = self._lookup(symbol)

        self._mass = None
        if mass:
            self._mass = mass

    def _lookup(self, identifier):
        """ Looks up element from symbol, name, or atomic number

        :param str or int identifier: Unique symbol, name, or atomic number of element
        """
        if isinstance(identifier, str):
            if re.match("^[A-Z][a-z]?$", identifier): # Symbol
                return self._db[identifier]
            elif re.match("^[A-Z][a-z]*$", identifier): # Name
                for symbol in self._db:
                    if self._db[symbol]['name'] == identifier:
                        return self._db[symbol]
            raise KeyError('symbol/name:{} does not exist'.format(identifier))
        elif isinstance(identifier, int): # Atomic Number
            for symbol in self._db:
                if self._db[symbol]['z'] == identifier:
                    return self._db[symbol]
            raise IndexError('z:{} does not exist'.format(identifier))
        raise NotImplementedError('identifier type:{} value:{} not recognized'.format(
            type(identifier), identifier))

    def __eq__(self, element):
        """ Test equality of elements 

        if symbol and mass are equal they are equal
        """
        if self.mass == element.mass and self.symbol == element.symbol:
            return True
        return False

    def __repr__(self):
        return "<Element symbol:{} name:{} mass:{:2.2f}>".format(
            self.symbol, self.name, self.mass)

    @property
    def mass(self):
        if self._mass:
            return self._mass
        return self._element['mass']

    @property
    def symbol(self):
        return self._element['symbol']

    @property
    def name(self):
        return self._element['name']


class Material:
    """ Material Representation """
    def __init__(self, stoichiometry):
        """Create Material from stoichiometry and density

        :param str or dict stoichiometry: stoichiometry of material
        :param float density: Density [g/cm^3] of material

        Stoichiometry can be specified in many ways. For strings check
        the regular expression.
          - 'SiC' 
          - 'CO2' 
          - 'Cu99.0Ni1.0' 
          - {'Cu': 99, 'Ni': 1.0} 
          - {Element('Cu'): 99, Element('Ni'): 1.0}

        """
        self.elements = {}

        single_int = '([A-Z][a-z]?)([0-9]*)'
        single_float = '([A-Z][a-z]?)([0-9]+(?:\.[0-9]*))?'
        if isinstance(stoichiometry, str):
            if re.match('^(?:{})+$'.format(single_int), stoichiometry):
                matches = re.findall(single_int, stoichiometry)
                for match in matches:
                    symbol, fraction = match
                    element = Element(symbol)
                    if fraction == '':
                        fraction = 1
                    if int(fraction) == 0:
                        raise ValueError('cannot have 0 of element {}'.format(symbol))
                    if element in self.elements:
                        error_str = 'cannot have duplicate elements {} in stoichiometry'
                        raise ValueError(error_str.format(symbol))
                    self.elements.update({element: float(fraction)})
            elif re.match('^(?:{})+$'.format(single_float), stoichiometry):
                matches = re.findall(single_float, stoichiometry)
                for match in matches:
                    symbol, fraction = match
                    element = Element(symbol)
                    if float(fraction) == 0.0:
                        raise ValueError('cannot have 0.0 of element {}'.format(symbol))
                    if element in elements:
                        error_str = 'cannot have duplicate elements {} in stoichiometry'
                        raise ValueError(error_str.format(symbol))
                    self.elements.update({element: float(fraction)})
            raise ValueError('stoichiometry str {} unrecognized'.format(stoichiometry))
        elif isinstance(stoichiometry, dict):
            for element in stoichiometry:
                if not isinstance(element, Element):
                    element = Element(element)
                self.elements.update({element: float(fraction)})
        else:
            raise NotImplementedError('stoichometry must be str or dict see doc')

        # Normalize the Chemical Composisiton to 1.0
        stoichiometry_sum = 0.0
        for element in self.elements:
            stoichiometry_sum += self.elements[element]
        for element in self.elements:
            self.elements[element] /= stoich_sum

    @property
    def chemical_formula(self):
        return ' '.join('{} {:1.2f}'.format(element.symbol, self.elements[element]) for element in self.elements)

    def __repr__(self):
        return "<Material formula:{} density:{:2.3f}>".format(self.chemical_formula, self.density)

    def __eq__(self, material):
        if abs(self.density - material.density) > 1e-6:
            return False
        for element in self.elements:
            if not element in material.elements:
                return False
            if self.elements[element] != materials.elements[element]:
                return False
        return True


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

