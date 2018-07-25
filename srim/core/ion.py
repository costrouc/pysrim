from math import sqrt

from . import units
from .element import Element

class Ion(Element):
    """ Representation of ion traveling through medium

    Similar to :class:`srim.core.element.Element` but associates an
    energy with the element.

    Parameters
    ----------
    identifier : :obj:`str`, :obj:`int`
        Symbol, Name, or Atomic Number of ion
    energy : :obj:`float`
        Energy [eV] of ion
    mass : :obj:`float`, optional
        Mass [amu] of element. Default is most common isotope atomic
        weight

    Examples
    --------
    Constructing a Helium Ion.

    >>> Ion('He', 1e6)
    "<Ion element:He mass:4.00 energy:1.00e6 eV>"

    >>> Ion('He', energy=1e6, mass=4.2)
    "<Ion element:He mass:4.20 energy:1.00e6 eV>"
    """
    def __init__(self, identifier, energy, mass=None):
        """Initialize Ion"""
        if energy <= 0.0:
            raise ValueError('energy {} cannot be 0.0 or less'.format(energy))

        self._energy = energy
        super(Ion, self).__init__(identifier, mass)

    def __repr__(self):
        return "<Ion element:{} mass:{:2.2f} energy:{:1.2E} eV>".format(
            self.name, self.mass, self.energy)

    @property
    def energy(self):
        """Ion's energy [eV]"""
        return self._energy

    @property
    def velocity(self):
        """Ion's velocity [m/s]"""
        return sqrt(2 * (self.energy * units.eV) / (self.mass * units.amu))
