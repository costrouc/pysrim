import pytest

from srim.core import Material

# Material Init
def test_material_init_int():
    material = Material.from_str('SiC', 1.0)


    
