import re

from .element import Element

class Material:
    """ Material Representation """
    def __init__(self, elements, density):
        """Create Material from elements and density

        :param dict elements: Dictionary of elements with fraction
        :param float density: Density [g/cm^3] of material

        Elements can be specified in two ways in dictionary.
          - {Element('Cu'): 99.0, Element('Ni'): 1.0}
          - {'Cu': 99.0, 'Ni': 1.0}
        """
        self.density = density
        self.elements = {}

        stoich_sum = 0.0
        for element in elements:
            if not isinstance(element, Element):
                element = Element(element)

            fraction = elements[element]
            stoich_sum += fraction
            if fraction <= 0.0:
                raise ValueError('cannot have {} of element {}'.format(
                    fraction, element.symbol))
            
            if element in self.elements:
                error_str = 'cannot have duplicate elements {} in stoichiometry'
                raise ValueError(error_str.format(element.symbol))

            self.elements.update({element: float(fraction)})

        # Normalize the Chemical Composisiton to 1.0
        for element in self.elements:
            self.elements[element] /= stoich_sum

    @classmethod        
    def from_str(cls, chemical_formula, density):
        """ Creation Material from chemical formula string and density

        :params str chemical_formula: Chemical formula string in specific format
        :params float density: Density [g/cm^3] of material

        Examples of chemical_formula:
         - SiC
         - CO2
         - AuFe1.5
         - Al10.0Fe90.0
        """
        single_element = '([A-Z][a-z]?)([0-9]*(?:\.[0-9]*))?'
        elements = {}

        if re.match('^(?:{})+$'.format(single_element), chemical_formula):
            matches = re.findall(single_element, chemical_formula)

        # Check for errors in stoichiometry
        for symbol, fraction in matches:
            element = Element(symbol)

            if element in elements:
                error_str = 'cannot have duplicate elements {} in stoichiometry'
                raise ValueError(error_str.format(element.symbol))

            if fraction == '':
                fraction = 1.0

            elements.update({element: float(fraction)})
        return Material(elements, density)
            
    @property
    def chemical_formula(self):
        return ' '.join('{} {:1.2f}'.format(element.symbol, self.elements[element]) for element in self.elements)

    def __repr__(self):
        material_str = "<Material formula:{} density:{:2.3f}>"
        return material_str.format(self.chemical_formula, self.density)

    def __eq__(self, material):
        if abs(self.density - material.density) > 1e-6:
            return False
        
        if len(self.elements) != len(material.elements):
            return False

        for element in self.elements:
            if not element in material.elements:
                return False
            if self.elements[element] != materials.elements[element]:
                return False
        return True
