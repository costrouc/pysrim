from .material import Material
from .utils import check_input, is_positive

class Layer(Material):
    """ Represents a layer in target

    """
    def __init__(self, elements, density, phase, width, name=None):
        
        self.width = width
        self.name = name
        super(Layer, self).__init__(elements, density, phase)

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
