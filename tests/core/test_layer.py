import pytest

from srim.core.layer import Layer
from srim.core.element import Element


def test_layer_init_simple():
    layer = Layer.from_formula('Ni99Fe1', density=1.0, width=1.0, phase=0, name='layer 1')
    assert layer.name == 'layer 1'
    assert layer.density == 1.0
    assert layer.width == 1.0
    assert layer.phase == 0
    assert len(layer.elements) == 2
    assert Element('Ni') in layer.elements
    assert Element('Fe') in layer.elements

