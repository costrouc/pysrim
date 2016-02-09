from .material import Material

class Layer(Material):
    """ Represents a layer in target

    """
    def __init__(self, elements, width):
        self.width = width
        super(Layer, self).__init__(elements)

    def __repr__(self):
        return "<Layer material:{} width:{}>".format(self.chemical_formula, self.width)
