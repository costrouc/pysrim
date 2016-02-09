from .elementdb import ElementDB

class Element(object):
    """ Element from periodic table

    """
    def __init__(self, identifier, mass=None):
        """ Initializes element from identifier and mass

        :param str or int identifier: Symbol, Name, or Atomic Number of element
        :param float mass: Mass [amu] of element
        """
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
        return self._symbol

    @property
    def name(self):
        return self._name

    @property
    def atomic_number(self):
        return self._atomic_number

    @property
    def mass(self):
        return self._mass

