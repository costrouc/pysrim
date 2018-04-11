import pytest

from srim.core.ion import Ion

# Test Ion Init
def test_init_symbol():
    ion = Ion('Au', 1.0)
    assert ion.symbol == 'Au'
    assert ion.name == 'Gold'
    assert ion.atomic_number == 79
    assert ion.energy == 1.0


def test_init_name():
    ion = Ion('Gold', 1.0)
    assert ion.symbol == 'Au'
    assert ion.name == 'Gold'
    assert ion.atomic_number == 79
    assert ion.energy == 1.0


def test_init_atomic_number():
    ion = Ion(79, 1.0)
    assert ion.symbol == 'Au'
    assert ion.name == 'Gold'
    assert ion.atomic_number == 79
    assert ion.energy == 1.0


def test_init_invalid_energy_zero():
    with pytest.raises(ValueError):
        Ion('Au', 0.0)


def test_init_invalid_energy_negative():
    with pytest.raises(ValueError):
        Ion('Au', -1.0)


# Test Ion Velocity
def test_ion_velocity():
    ion = Ion('Au', 1.0)                                # Energy [eV]
    assert abs(ion.velocity - 989.8041041365332) < 1e-6 # Velocity [m/s]
