# srim-python

<table>
<tr>
  <td>Latest Release</td>
  <td><img src="https://img.shields.io/pypi/v/pysrim.svg" alt="latest release" /></td>
</tr>
<tr>
  <td>Package Status</td>
  <td><img src="https://img.shields.io/pypi/status/pysrim.svg" alt="status" /></td>
</tr>
<tr>
  <td>License</td>
  <td><img src="https://img.shields.io/pypi/l/pysrim.svg" alt="license" /></td>
</tr>
<tr>
  <td>Build Status</td>
  <td>
    <a href="https://gitlab.com/costrouc/srim-python/pipelines">
    <img src="https://gitlab.com/costrouc/srim-python/badges/master/pipeline.svg" alt="gitlab pipeline status" />
    </a>
  </td>
</tr>
<tr>
  <td>Coverage</td>
  <td><img src="https://gitlab.com/costrouc/srim-python/badges/master/coverage.svg" alt="coverage" /></td>
</tr>
<tr>
  <td>Documentation</td>
  <td>
    <a href="https://pysrim.readthedocs.io/en/latest/">
    <img src="https://readthedocs.org/projects/pysrim/badge/?version=latest" alt="readthedocs documentation" />
    </a>
  </td>
</tr>
</table>


A package for automating SRIM input and output analysis.

![srim heatmap](https://gitlab.com/costrouc/srim-python/raw/master/examples/images/length-heatmap-log.png)

# Features

## Automate running SRIM with Windows and Linux (wine)

`/tmp/srim` is the path to the SRIM executable directory. `pysrim`
will add all the necessary input files. If this ran successfully for
you a SRIM window will popup and start the calculation. If a plot of
the cascade is showing make sure to minimize it to speed it up!

Also some advice. Since you can automate the calculation, it is nice
to break the calculation into several pieces so that if it crashes you
do not lose all your results. For example if you need to do 10,000
ions maybe break it into 1,000 ions x 10 calculations. We all know
that SRIM has a tendancy to crash at the worst times...

``` python
ion = Ion('Ni', energy=3.0e6)
layer = Layer({
        'Ni': {
            'stoich': 1.0,
            'E_d': 30.0,
            'lattice': 0.0,
            'surface': 3.0
        }}, density=8.9, width=20000.0)
target = Target([layer])
srim = SRIM(target, ion, number_ions=100, calculation=1) # Calculation=2 => full cascade
results = srim.run('/tmp/srim')
```

## Copy SRIM output files to directory

After a SRIM calculation has completed run `copy_output_files` to take
all of the output files and move them to a directory of your liking.

``` python
SRIM.copy_output_files('/tmp/srim', '/home/costrouc/scratch/srim')
```

## Post processes SRIM output as numpy arrays

`srim-python` was not designed to create nice plots for you becuase
this would never be flexible enough for your use case. Instead
`srim-python` provides classes with properties for each column of the
output results file as nice numpy arrays. The posibilities are endless
at this point.

``` python
def plot_damage_energy(folder, ax):
    phon = Phonons(folder)
    dx = max(phon.depth) / 100.0
    energy_damage = (phon.ions + phon.recoils) * dx
    ax.plot(phon.depth, energy_damage / phon.num_ions, label='{}'.format(folder))
    return sum(energy_damage)

def plot_ionization(folder, ax):
    ioniz = Ioniz(folder)
    dx = max(ioniz.depth) / 100.0
    ax.plot(ioniz.depth, ioniz.ions, label='Ionization from Ions')
    ax.plot(ioniz.depth, ioniz.recoils, label='Ionization from Recoils')
```

Set `folders` to list of directories to SRIM outputs. See
[Analysis](https://gitlab.com/costrouc/srim-python/blob/master/examples/notebooks/Analysis.ipynb)
for detailed example. Notice how there is a python class for each SRIM
output file and gives simple access to each column. This did require
some complex regex to get working just right.

``` python
fig, ax = plt.subplots(1, len(folders), sharey=True, sharex=True)

for i, folder in enumerate(folders):
    plot_damage_energy(folder, ax[i])
    plot_ionization(folder, ax[i])
    ax[i].legend()
    ax[i].set_ylabel('eV')
    ax[i].set_xlabel('Depth [Angstroms]')
fig.suptitle('Ionization Energy vs Depth', fontsize=15)
fig.set_size_inches((10, 4))
fig.tight_layout()
```

![srim heatmap](https://gitlab.com/costrouc/srim-python/raw/master/examples/images/ionization-vs-depth.png)

See [jupyter
notebook](<https://gitlab.com/costrouc/srim-python/blob/master/examples/notebooks/Analysis.ipynb)
for full demonstration of features.

An example of creating some publication graphics with pysrim can also
be found in that
[directory](https://gitlab.com/costrouc/srim-python/blob/master/examples/notebooks/SiC.ipynb). I
have used this in a
[publication](https://doi.org/10.1016/j.cossms.2017.09.003).


# Installation

## Linux

SRIM can run perfectly on linux with `wine <https://www.winehq.org/>`_

Run the `installation script <https://gitlab.com/costrouc/srim-python/raw/master/install.sh>`_ with bash.

Click extract and then done.

## Windows

A collegue of mine has gotten it to work easily on Windows but I
myself have no experience. It should just work if you point the
package to the SRIM executable.

# Contributing

All contributions, bug reports, bug fixes, documentation improvements,
enhancements and ideas are welcome!

# License

MIT
