import pytest

from srim.srim import SRIM
from srim.core.target import Target
from srim.core.layer import Layer
from srim.core.ion import Ion

def test_simple_init():
    ion = Ion('Ni', 1.0e6)

    layer = Layer.from_formula('Ni', 8.9, 1000.0)
    target = Target([layer])

    srim = SRIM(target, ion)

