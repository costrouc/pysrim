import pytest

from srim.core.element import Element

# Element Initialization
def test_init_mass_default():
    element = Element('Au')
    assert abs(element.mass - 196.966995239) < 1e-8

def test_init_set_mass():
    element = Element('Au', 1.0)
    assert element.mass == 1.0

def test_init_symbol():
    element = Element('Au')
    assert element.symbol == 'Au'
    assert element.name == 'Gold'
    assert element.atomic_number == 79
    assert abs(element.mass - 196.966995239) < 1e-8

def test_init_name():
    element = Element('Gold')
    assert element.symbol == 'Au'
    assert element.name == 'Gold'
    assert element.atomic_number == 79
    assert abs(element.mass - 196.966995239) < 1e-8

def test_init_atomic_number():
    element = Element(79)
    assert element.symbol == 'Au'
    assert element.name == 'Gold'
    assert element.atomic_number == 79
    assert abs(element.mass - 196.966995239) < 1e-8


# Element equality
def test_equality_eqaul():
    element1 = Element('Au', 2.0)
    element2 = Element('Au', 2.0)
    assert element1 == element2

def test_equality_not_equal():
    element1 = Element('H')
    element2 = Element('Au')
    assert element1 != element2
