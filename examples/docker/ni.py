import os

from srim import Ion, Layer, Target, TRIM

# Construct a 3MeV Nickel ion
ion = Ion('Ni', energy=3.0e6)

# Construct a layer of nick 20um thick with a displacement energy of 30 eV
layer = Layer({
        'Ni': {
            'stoich': 0.5,
            'E_d': 30.0,
            'lattice': 0.0,
            'surface': 3.0
        }, 'Au': {'stoich': 0.5, 'E_d': 25.0, 'lattice': 0.0, 'surface': 3.0}}, density=8.9, width=20000.0)

# Construct a target of a single layer of Nickel
target = Target([layer])

# Initialize a TRIM calculation with given target and ion for 25 ions, quick calculation
trim = TRIM(target, ion, number_ions=100000, calculation=1)

# Specify the directory of SRIM.exe
# For windows users the path will include C://...
srim_executable_directory = '/tmp/srim'

# takes about 10 seconds on my laptop
results = trim.run(srim_executable_directory)
# If all went successfull you should have seen a TRIM window popup and run 25 ions!
# results is `srim.output.Results` and contains all output files parsed

os.makedirs('/tmp/output', exist_ok=True)
TRIM.copy_output_files('/tmp/srim', '/tmp/output')
