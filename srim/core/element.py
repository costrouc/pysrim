from .elementdb import ElementDB

class Element(object):
    """ Element from periodic table

    Parameters
    ----------
    identifier : :obj:`str`, :obj:`int`
        Symbol, Name, or Atomic Number of element
    mass : :obj:`float`, optional
        Mass [amu] of element. Default is most common isotope atomic
        weight

    Examples
    --------
    Constructing a Helium Atom.

    >>> Element('He')
    <Element symbol:He name:Helium mass:4.00>

    >>> Element('Helium')
    <Element symbol:He name:Helium mass:4.00>

    >>> Element(2)
    <Element symbol:He name:Helium mass:4.00>

    >>> Element('He', 4.3)
    <Element symbol:He name:Helium mass:4.30>
    """
    def __init__(self, identifier, mass=None):
        """Initializes element from identifier and mass"""
        element = ElementDB.lookup(identifier)

        self._symbol = element['symbol']
        self._name = element['name']
        self._atomic_number = element['z']

        if mass:
            self._mass = mass
        else:
            self._mass = element['mass']

    def __eq__(self, element):
        if (self.symbol == element.symbol and
            self.name == element.name and
            self.atomic_number == element.atomic_number and
            self.mass == element.mass):
            return True
        return False

    def __repr__(self):
        return "<Element symbol:{} name:{} mass:{:2.2f}>".format(
            self.symbol, self.name, self.mass)

    def __hash__(self):
        return sum(hash(item) for item in [
            self._mass, self._symbol, self._name, self.atomic_number
        ])

    @property
    def symbol(self):
        """Element's atomic symbol"""
        return self._symbol

    @property
    def name(self):
        """Element's formal name"""
        return self._name

    @property
    def atomic_number(self):
        """Element's atomic number"""
        return self._atomic_number

    @property
    def mass(self):
        """Element's mass"""
        return self._mass
