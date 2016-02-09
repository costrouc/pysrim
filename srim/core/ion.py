from math import sqrt

from . import units
from .element import Element

class Ion(Element):
    """ Ion traveling through medium

    """
    def __init__(self, identifier, energy, mass=None):
        """Initialize Ion

        :param int or str symbol: Atomic symbol of element
        :param float energy: Energy [eV] of ion
        :param float mass: Mass [amu] of ion
        """
        if energy <= 0.0:
            raise ValueError('energy {} cannot be 0.0 or less'.format(energy))

        self._energy = energy
        super(Ion, self).__init__(identifier, mass)

    def __repr__(self):
        return "<Ion element:{} mass:{} energy:{} keV>".format(
            self.name, self.mass, self.energy)

    @property
    def energy(self):
        return self._energy

    @property
    def velocity(self):
        """ Velocity of Ion [m/s] """
        return sqrt(2 * (self.energy * units.eV) / (self.mass * units.amu))

