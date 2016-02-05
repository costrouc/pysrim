from .material import Material

class Layer(Material):
    """ Represents a layer in target

    """
    def __init__(self, material, width):
        self.width = width
        super().__init__(material)

    def __repr__(self):
        return "<Layer material:{} width:{}>".format(self.chemical_formula, self.width)
