class Target(object):
    """ Target that Ion impacts

    """
    def __init__(self, layers):
        self.layers = layers

    @property
    def width(self):
        """ total width of target """
        return sum(layer.width for layer in self.layers)
