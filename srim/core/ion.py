from math import sqrt

from . import units
from .element import Element

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
