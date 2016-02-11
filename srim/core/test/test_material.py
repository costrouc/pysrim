import pytest

from srim.core.element import Element
from srim.core.material import Material


# Material Init
@pytest.mark.parametrize("elements, check", [
    ({Element('Au'): 1.0}, (1.0, 25.0, 0.0, 3.0)),
    ({'Au': 1.0}, (1.0, 25.0, 0.0, 3.0)),
    ({Element('Au'): [1.0]}, (1.0, 25.0, 0.0, 3.0)),
    ({'Au': [1.0]}, (1.0, 25.0, 0.0, 3.0)),
    ({'Au': [1.0, 30.0, 1.0, 1.0]}, (1.0, 30.0, 1.0, 1.0)),
    ({Element('Au'): {'stoich': 1.0}}, (1.0, 25.0, 0.0, 3.0)),
    ({'Au': {'stoich': 1.0}}, (1.0, 25.0, 0.0, 3.0)),
    ({'Au': {'stoich': 1.0, 'E_d': 30.0, 'lattice': 1.0, 'surface': 1.0}}, (1.0, 30.0, 1.0, 1.0))
])
def test_init_simple_prenormalized(elements, check):
    element = Element('Au')
    material = Material(elements, 1.0)
    
    assert len(material.elements) == 1
    assert element in material.elements
    assert abs(material.elements[element]['stoich'] - check[0]) < 1e-6
    assert abs(material.elements[element]['E_d'] - check[1]) < 1e-6
    assert abs(material.elements[element]['lattice'] - check[2]) < 1e-6
    assert abs(material.elements[element]['surface'] - check[3]) < 1e-6
    assert material.density == 1.0

def test_init_single_normalize():
    element = Element('Au')
    material = Material({element: 2.0}, 1.0)

    assert len(material.elements) == 1
    assert element in material.elements
    assert abs(material.elements[element]['stoich'] - 1.0) < 1e-6
    assert abs(material.elements[element]['E_d'] - 25.0) < 1e-6
    assert abs(material.elements[element]['lattice'] - 0.0) < 1e-6
    assert abs(material.elements[element]['surface'] - 3.0) < 1e-6
    assert material.density == 1.0


def test_init_single_invalid_stoich_zero():
    with pytest.raises(ValueError):
        Material({'Au': 0.0}, 1.0)


def test_init_single_invalid_frac_negative():
    with pytest.raises(ValueError):
        Material({'Au': -0.1}, 1.0)


def test_init_multiple():
    element1 = Element('Au')
    element2 = Element('Fe')
    material = Material({element1: 0.5, element2: 0.5}, 1.0)

    assert len(material.elements) == 2
    assert element1 in material.elements
    assert abs(material.elements[element1]['stoich'] - 0.5) < 1e-6
    assert element2 in material.elements
    assert abs(material.elements[element2]['stoich'] - 0.5) < 1e-6
    assert material.density == 1.0


def test_init_formula_FeAl():
    element1 = Element('Fe')
    element2 = Element('Al')
    material = Material.from_formula('Fe10.0Al90.0', 1.0)

    assert len(material.elements) == 2
    assert element1 in material.elements
    assert abs(material.elements[element1]['stoich'] - 0.1) < 1e-6
    assert element2 in material.elements
    assert abs(material.elements[element2]['stoich'] - 0.9) < 1e-6
    assert material.density == 1.0

def test_init_formula_FeAl_floats():
    element1 = Element('Fe')
    element2 = Element('Al')
    material = Material.from_formula('Fe0.1Al.9', 1.0)

    assert len(material.elements) == 2
    assert element1 in material.elements
    assert abs(material.elements[element1]['stoich'] - 0.1) < 1e-6
    assert element2 in material.elements
    assert abs(material.elements[element2]['stoich'] - 0.9) < 1e-6
    assert material.density == 1.0


def test_init_invalid_formula_SiSi():
    with pytest.raises(ValueError):
        Material.from_formula('SiSi', 1.0)


# Test equality material
def test_material_equality_equal():
    material1 = Material.from_formula('Fe0.1Al0.9', 1.0)
    material2 = Material({Element('Fe'): 0.1, Element('Al'): 0.9}, 1.0)

    assert material1 == material2

def test_material_equality_not_equal_density():
    element1 = Element('Fe')
    element2 = Element('Al')
    material1 = Material.from_formula('Fe0.1Al0.9', 1.0)
    material2 = Material({element1: 0.1, element2: 0.9}, 2.0)

    assert material1 != material2

def test_material_equality_not_equal_stoich():
    element1 = Element('Fe')
    element2 = Element('Al')
    material1 = Material.from_formula('Fe0.2Al0.8', 1.0)
    material2 = Material({element1: 0.1, element2: 0.9}, 1.0)

    assert material1 != material2

def test_material_equality_not_equal_elements():
    element1 = Element('Fe')
    element2 = Element('Al')
    material1 = Material.from_formula('Sn0.1Al0.9', 1.0)
    material2 = Material({element1: 0.1, element2: 0.9}, 1.0)

    assert material1 != material2


def test_material_equality_not_equal_num_elements():
    element1 = Element('Fe')
    element2 = Element('Al')
    material1 = Material.from_formula('Fe0.2Al0.8Au1.0', 1.0)
    material2 = Material({element1: 0.1, element2: 0.9}, 1.0)

    assert material1 != material2
    
