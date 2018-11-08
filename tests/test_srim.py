from srim.srim import TRIM, SR
from srim.core.target import Target
from srim.core.layer import Layer
from srim.core.ion import Ion

TESTDATA_DIRECTORY = 'test_files'

def test_simple_trim_init():
    ion = Ion('Ni', 1.0e6)

    layer = Layer.from_formula('Ni', 8.9, 1000.0)
    target = Target([layer])

    trim = TRIM(target, ion)


def test_simple_srim_init():
    # Construct a Nickel ion
    ion = Ion('Xe', energy=1.2e9)

    # Construct a layer of nick 20um thick with a displacement energy of 30 eV
    layer = Layer({
        'Si': {
            'stoich': 0.5,
            'E_d': 35.0, # Displacement Energy
            'lattice': 0.0,
            'surface': 3.0
        },
        'C': {
            'stoich': 0.5,
            'E_d': 20.0, # Displacement Energy
            'lattice': 0.0,
            'surface': 3.0
        }
    }, density=3.21, width=10000.0)

    target = Target([layer])

    srim = SR(layer, ion, output_type=5)

    # resulting file should be equal to
    # test_files/SRIM/SR_OUTPUT.txt
