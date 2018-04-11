import pytest

from srim.core.target import Target
from srim.core.layer import Layer


def test_init_simple():
    layer1 = Layer.from_formula('Ni99Fe1', density=1.0, width=1.0)
    layer2 = Layer.from_formula('Au', density=1.0, width=2.0)
    target = Target([layer1, layer2])
    assert target.width == 3.0
