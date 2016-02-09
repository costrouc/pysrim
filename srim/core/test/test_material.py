import pytest

from srim.core.element import Element
from srim.core.material import Material


# Material Init
def test_init_single():
    element = Element('Au')
    material = Material({element: 1.0}, 1.0)

    assert len(material.elements) == 1
    assert element in material.elements
    assert abs(material.elements[element] - 1.0) < 1e-6
    assert material.density == 1.0


def test_init_single_element_str():
    element = Element('Au')
    material = Material({'Au': 1.0}, 1.0)

    assert len(material.elements) == 1
    assert element in material.elements
    assert abs(material.elements[element] - 1.0) < 1e-6
    assert material.density == 1.0


def test_init_single_normalize():
    element = Element('Au')
    material = Material({element: 2.0}, 1.0)

    assert len(material.elements) == 1
    assert element in material.elements
    assert abs(material.elements[element] - 1.0) < 1e-6
    assert material.density == 1.0


def test_init_single_invalid_frac_zero():
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
    assert abs(material.elements[element1] - 0.5) < 1e-6
    assert element2 in material.elements
    assert abs(material.elements[element2] - 0.5) < 1e-6
    assert material.density == 1.0


def test_init_multiple_str():
    element1 = Element('Au')
    element2 = Element('Fe')
    material = Material({'Au': 0.5, element2: 0.5}, 1.0)

    assert len(material.elements) == 2
    assert element1 in material.elements
    assert abs(material.elements[element1] - 0.5) < 1e-6
    assert element2 in material.elements
    assert abs(material.elements[element2] - 0.5) < 1e-6
    assert material.density == 1.0


def test_init_multiple_normalize():
    element1 = Element('Au')
    element2 = Element('Fe')
    material = Material({element1: 5.0, element2: 5.0}, 1.0)

    assert len(material.elements) == 2
    assert element1 in material.elements
    assert abs(material.elements[element1] - 0.5) < 1e-6
    assert element2 in material.elements
    assert abs(material.elements[element2] - 0.5) < 1e-6
    assert material.density == 1.0


# Material String Init
def test_init_formula_Si():
    element = Element('Si')
    material = Material.from_str('Si', 1.0)

    assert len(material.elements) == 1
    assert element in material.elements
    assert abs(material.elements[element] - 1.0) < 1e-6


def test_init_formula_SiC():
    element1 = Element('Si')
    element2 = Element('C')
    material = Material.from_str('SiC', 1.0)

    assert len(material.elements) == 2
    assert element1 in material.elements
    assert abs(material.elements[element1] - 0.5) < 1e-6
    assert element2 in material.elements
    assert abs(material.elements[element2] - 0.5) < 1e-6
    assert material.density == 1.0

def test_init_formula_CO2():
    element1 = Element('C')
    element2 = Element('O')
    material = Material.from_str('CO2', 1.0)

    assert len(material.elements) == 2
    assert element1 in material.elements
    assert abs(material.elements[element1] - 1.0/3.0) < 1e-6
    assert element2 in material.elements
    assert abs(material.elements[element2] - 2.0/3.0) < 1e-6
    assert material.density == 1.0

def test_init_formula_FeAl():
    element1 = Element('Fe')
    element2 = Element('Al')
    material = Material.from_str('Fe10.0Al90.0', 1.0)

    assert len(material.elements) == 2
    assert element1 in material.elements
    assert abs(material.elements[element1] - 0.1) < 1e-6
    assert element2 in material.elements
    assert abs(material.elements[element2] - 0.9) < 1e-6
    assert material.density == 1.0

def test_init_formula_FeAl_floats():
    element1 = Element('Fe')
    element2 = Element('Al')
    material = Material.from_str('Fe0.1Al.9', 1.0)

    assert len(material.elements) == 2
    assert element1 in material.elements
    assert abs(material.elements[element1] - 0.1) < 1e-6
    assert element2 in material.elements
    assert abs(material.elements[element2] - 0.9) < 1e-6
    assert material.density == 1.0

def test_init_invalid_formula_SiSi():
    with pytest.raises(ValueError):
        Material.from_str('SiSi', 1.0)


# Test equality material
def test_material_equality_equal():
    material1 = Material.from_str('Fe0.1Al0.9', 1.0)
    material2 = Material({Element('Fe'): 0.1, Element('Al'): 0.9}, 1.0)

    assert material1 == material2

def test_material_equality_not_equal_density():
    element1 = Element('Fe')
    element2 = Element('Al')
    material1 = Material.from_str('Fe0.1Al0.9', 1.0)
    material2 = Material({element1: 0.1, element2: 0.9}, 2.0)

    assert material1 != material2

def test_material_equality_not_equal_stoich():
    element1 = Element('Fe')
    element2 = Element('Al')
    material1 = Material.from_str('Fe0.2Al0.8', 1.0)
    material2 = Material({element1: 0.1, element2: 0.9}, 1.0)

    assert material1 != material2

def test_material_equality_not_equal_elements():
    element1 = Element('Fe')
    element2 = Element('Al')
    material1 = Material.from_str('Sn0.1Al0.9', 1.0)
    material2 = Material({element1: 0.1, element2: 0.9}, 1.0)

    assert material1 != material2


def test_material_equality_not_equal_num_elements():
    element1 = Element('Fe')
    element2 = Element('Al')
    material1 = Material.from_str('Fe0.2Al0.8Au1.0', 1.0)
    material2 = Material({element1: 0.1, element2: 0.9}, 1.0)

    assert material1 != material2
    
