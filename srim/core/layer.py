from .material import Material
from .utils import check_input, is_positive

class Layer(Material):
    """ Represents a layer in target

    """
    def __init__(self, elements, density, width, phase=0, name=None):
        """ Creation of Layer from elements, density, width, phase, and name

        :params float width: width [Ang] of layer
        :params str name: Name of the Layer (defaults to chemical_formula)
        
        See Material for documentation on elements, density, and phase parameters
        """
        self.width = width
        self.name = name
        super(Layer, self).__init__(elements, density, phase)

    @classmethod
    def from_formula(cls, chemical_formula, density, width, phase=0, name=None):
        """ Creation Layer from chemical formula string, density, width, phase, and name

        :params float width: width [Ang] of layer
        :params str name: Name of the Layer (defaults to chemical_formula)

        See Material for documentation on chemical_formula, density, and phase parameters
        """
        elements = cls._formula_to_elements(chemical_formula)
        return Layer(elements, density, width, phase, name)

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = check_input(float, is_positive, value)

    @property
    def name(self):
        if self._name:
            return self._name
        return self.chemical_formula

    @name.setter
    def name(self, value):
        self._name = str(value)

    def __repr__(self):
        return "<Layer material:{} width:{}>".format(self.chemical_formula, self.width)
