import yaml
import os
import re

import srim


def create_elementdb():
    dbpath = os.path.join(srim.__path__[0], 'data', 'elements.yaml')
    return yaml.load(open(dbpath, "r"))


class ElementDB(object):
    """Element database at ``srim.data.elements.yaml``"""
    _db = create_elementdb()

    @classmethod
    def lookup(cls, identifier):
        """ Looks up element from symbol, name, or atomic number

        Parameters
        ----------
        identifier : :obj:`str`, :obj:`int`
            Unique symbol, name, or atomic number of element

        Notes
        -----
            This class is used for creation of elements, ions,
            etc. but generally will not be needed by the user.
        """
        if isinstance(identifier, (bytes, str)):
            if re.match("^[A-Z][a-z]?$", identifier):   # Symbol
                return cls._lookup_symbol(identifier)
            elif re.match("^[A-Z][a-z]*$", identifier): # Name
                return cls._lookup_name(identifier)
        elif isinstance(identifier, int):               # Atomic Number
            return cls._lookup_atomic_number(identifier)
        raise ValueError('identifier of type:{} value:{} not value see doc'.format(
            type(identifier), identifier))

    @classmethod
    def _lookup_symbol(cls, symbol):
        """ Looks up symbol in element database

        :param str symbol: Symbol of atomic element
        """
        return cls._db[symbol]

    @classmethod
    def _lookup_name(cls, name):
        """ Looks element in database by name

        :param str name: (Full) Name of atomic element (British spelling)
        """
        for symbol in cls._db:
            if cls._db[symbol]['name'] == name:
                return cls._db[symbol]
        raise KeyError('name:{} does not exist'.format(name))

    @classmethod
    def _lookup_atomic_number(cls, atomic_number):
        """ Look up element in database by atomic number (Z)

        :param int atomic_number: Atomic number of atomic element
        """
        for symbol in cls._db:
            if cls._db[symbol]['z'] == atomic_number:
                return cls._db[symbol]
        raise IndexError('atomic number:{} does not exist'.format(atomic_number))
