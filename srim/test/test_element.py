import pytest

from srim.core import Element

# Element Initialization
def test_element_init_symbol():
    element = Element('Fe')
    assert element.symbol == 'Fe'
    assert element.name == 'Iron'

def test_element_init_invalid_symbol():
    with pytest.raises(KeyError):
        Element('Zx')

def test_element_init_name():
    element = Element('Aluminium')
    assert element.symbol == 'Al'
    assert element.name == 'Aluminium'

def test_element_init_invalid_name():
    with pytest.raises(KeyError):
        Element('Macium') # My gf's name

def test_element_init_atomic_number():
    element = Element(100)
    assert element.symbol == 'Fm'
    assert element.name == 'Fermium'

def test_element_init_invalid_atomic_number_negative():
    with pytest.raises(IndexError):
        Element(-1)

def test_element_init_invalid_atomic_number_large():
    with pytest.raises(IndexError):
        Element(130)

def test_element_init_mass_default():
    element = Element('H')
    assert abs(element.mass - 1.00794005394) < 1e-6

def test_element_init_set_mass():
    element = Element('Au', 1.0)
    assert element.mass == 1.0

# Element DataBase
def test_element_db_number():   # This test could be more extensive
    element = Element('Au')
    assert len(element._db) == 112

# Element equality
def test_element_equality_equal():
    element1 = Element('Au', 2.0)
    element2 = Element('Au', 2.0)
    assert element1 == element2

def test_element_equality_not_equal():
    element1 = Element('H')
    element2 = Element('Au')
    assert element1 != element2
