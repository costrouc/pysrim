import pytest

from srim.core import Element

def test_element_init_symbol():
    element = Element('Fe')
    assert element.symbol == 'Fe'
    assert element.name == 'Iron'
