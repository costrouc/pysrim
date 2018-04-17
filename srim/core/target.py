class Target(object):
    """ Target that Ion Impacts

    Parameters
    ----------
    layers : list
        list of :class:`srim.core.layer.Layer` to construct Target

    Examples
    --------
    Lets construct a SiC target. While only one layer is shown an
    arbitrary number of them can be used.

    >>> Target([Layer({
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
    }, density=3.21, width=10000.0)])
    """
    def __init__(self, layers):
        self.layers = layers

    @property
    def width(self):
        """total width of target (sum of layers)"""
        return sum(layer.width for layer in self.layers)
