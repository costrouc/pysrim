from .material import Material
from .utils import check_input, is_positive

class Layer(Material):
    """ Represents a layer in target

    Parameters
    ----------
    elements : :obj:`dict`
        dictionary of elements (:class:`srim.core.elements.Element`, :obj:`str`, or :obj:`int`) with properties
         - ``stoich``  (float, int, required): Stoichiometry of element (fraction)
         - ``E_d``     (float, int, optional): Displacement energy [eV] default 25.0 eV
         - ``lattice`` (float, int, optional): Lattice binding energies [eV] default 0.0 eV
         - ``surface`` (float, int, optional): Surface binding energies [eV] default 3.0 eV
    density : :obj:`float`
       density [g/cm^3] of material
    width : :obj:`float`
       width [Angstroms] of layer
    phase : :obj:`int`
       phase of material (solid = 0, gas = 1). Default solid (0).
    name : :obj:`str:, optional
       name of the Layer (defaults to chemical_formula)

    Examples
    --------
    Construct a layer of SiC with experimental values.

    >>> Layer({
        'Si': {
           'stoich': 0.5,
           'E_d': 35.0, # Displacement Energy [eV]
           'lattice': 0.0,
           'surface': 3.0
        },
        'C': {
           'stoich': 0.5,
           'E_d': 20.0, # Displacement Energy [eV]
           'lattice': 0.0,
           'surface': 3.0
    }, density=3.21, width=10000.0)
    """
    def __init__(self, elements, density, width, phase=0, name=None):
        """Creation of Layer from elements, density, width, phase, and
name"""
        self.width = width
        self.name = name
        super(Layer, self).__init__(elements, density, phase)

    @classmethod
    def from_formula(cls, chemical_formula, density, width, phase=0, name=None):
        """ Creation Layer from chemical formula string, density, width, phase, and name

        Parameters
        ----------
        chemical_formula : str
            see :meth:`srim.core.material.Material.from_formula` for
            allowed formulas. Quite flexible.
        density : :obj:`float`
            density [g/cm^3] of material
        width : :obj:`float`
            width [Angstroms] of layer
        phase : :obj:`int`
            phase of material (solid = 0, gas = 1). Default solid (0).
        name : :obj:`str:, optional
            name of the Layer (defaults to chemical_formula)

        Notes
        -----
            This method is not used as much since you do not have an
            easy way to set the displacement energy.
        """
        elements = cls._formula_to_elements(chemical_formula)
        return Layer(elements, density, width, phase, name)

    @property
    def width(self):
        """Layer's width"""
        return self._width

    @width.setter
    def width(self, value):
        self._width = check_input(float, is_positive, value)

    @property
    def name(self):
        """Layer's Name"""
        if self._name:
            return self._name
        return self.chemical_formula

    @name.setter
    def name(self, value):
        self._name = str(value)

    def __repr__(self):
        return "<Layer material:{} width:{}>".format(self.chemical_formula, self.width)
