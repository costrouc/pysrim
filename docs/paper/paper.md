---
title: "pysrim: Automation, Analysis, and Plotting of SRIM Calculations"
tags:
  - SRIM
  - nuclear materials
  - simulation
  - monte carlo
  - python
authors:
  - name: Christopher Ostrouchov
    orcid: 0000-0002-8734-4564
    affiliaton: 1
  - name: Yanwen Zhang
    orcid: 0000-0000-0000-0000
    affiliation: 2
  - name: William Weber
    orcid: 0000-0000-0000-0000
    affiliation: "1, 2"
affiliations:
  - name: "Department of Material Science and Engineering, University of Tennessee"
    index: 1
  - name: "Division Materials Science and Technology, Oak Ridge National Laboratory"
    index: 2
date: 18 April 2018
bibliography: paper.bib
---

# Summary

The behavior of ions traveling through a material is of great interest
to many fields. For instance, radiation damage in nuclear materials
and ion beam modification of materials are most concerned with
understanding the formation and evolution of defects along the ion
path [@was2016fundamentals]. Some of the important properties that can
be gleaned from investigating the initial damage from the ion include:
numbers of interstitials and vacancies produced, energy deposited per
unit length to electrons and atomic nuclei, track diameter, and
implanted ion profile. These properties enable further simulations and
allow computing a common unit of radiation damage dose, displacements
per atom (dpa), which can be used to compare irradiation experiments
with different ions [@backman2013molecular]
[@stoller2013use]. Additionally, the ejection of materials near the
surface due to incident ions is important to sputtering and ion-beam
analysis techniques, such as elastic recoil detection analysis (ERDA)
and secondary ion mass spectrometry (SIMS)
[@vickerman2011surface]. The interaction of ions within a material can
be broken into two parts: electronic and nuclear stopping. Electronic
stopping is the energy lost from the ion due to inelastic collisions
with electrons along its path. Nuclear stopping is the energy lost due
to elastic collisions between the ion and atomic nuclei within the
material.

The Stopping and Range of Ions in Matter (SRIM) code is a well known
software in the radiation damage and ion-beam communities that allows
the simulation, via Monte Carlo, of ions through a material by
modeling the energy transfer through electronic and nuclear stopping
[@ziegler2010srim]. SRIM was originally developed in 1985 and has had
numerous updates on the electronic stopping powers since then, with
the nuclear stopping well explained by the ZBL potential
[@ziegler1988stopping]. The executable SRIM is free to use for
non-commercial use but the source code is not available to the
community despite requests. While SRIM is a scientifically accurate
code it does not get updated frequently and has many bugs from a
usability standpoint.

# Pysrim

`pysrim` is a python library for automating SRIM calculations,
analysis, and for publication quality plotting. It is a continuously
delivered, tested, and fully-documented module. In addition, the
documentation includes several jupyter notebooks for getting started.

The first pain point that `pysrim` aims to solve is running the SRIM
calculation. SRIM has some well known limitations such as crashing
with large simulations and bad input values, only running on Windows,
and needing to be run interactively with user input. `pysrim` solves
this by: 1) having an api compatible with windows, linux, and OS X; 2)
having support for chunking of large calculations; and 3) recovering
from SRIM crashes. Along with cross platform support, a Docker
container image using `pysrim` has been constructed that allows SRIM
to run on a linux server without a display determined from benchmarks
to be around 50% faster. All of these features allow SRIM to be fully
automated via `pysrim`.

After running these calculations SRIM will produce many output files
all of which are not convenient to parse. Traditionally research
groups have copy and pasted sections into excel or other spreadsheets
for analysis. `pysrim` hopes to solve this by providing parsers for
all the major output files. These output files include:
[IONIZ.txt](https://pysrim.readthedocs.io/en/latest/source/srim.html#srim.output.Ioniz),
[VACANCY.txt](https://pysrim.readthedocs.io/en/latest/source/srim.html#srim.output.Vacancy),
[NOVAC.txt](https://pysrim.readthedocs.io/en/latest/source/srim.html#srim.output.NoVacancy),
[E2RECOIL.txt](https://pysrim.readthedocs.io/en/latest/source/srim.html#srim.output.EnergyToRecoils),
[PHONON.txt](https://pysrim.readthedocs.io/en/latest/source/srim.html#srim.output.Phonons),
[RANGE.txt](https://pysrim.readthedocs.io/en/latest/source/srim.html#srim.output.Range),
and
[COLLISON.txt](https://pysrim.readthedocs.io/en/latest/source/srim.html#srim.output.Collision). Once
the output file is parsed the data is available in `numpy`
arrays. From here the user is free to create plots of interesting
relationships in their data. `pysrim` additionally provides plotting
utilities for producing figures commonly needed in characterizing the
defect production distribution under ion irradiation for evaluating
radiation damage or ion beam modification in materials. This software
has been used for the SRIM calculations, analysis, and plotting in two
publications [@zhang2017coupled] [@zhang2014effect].

![Plots produced by `pysrim` of vacancies for ions traveling through
$SiC$. (top) 21 MeV $Si$ ion (bottom) 21 MeV $Ni$
ion](length-heatmap-log-cropped.png)

# Acknowledgements

CO acknowledges support from the University of Tennessee Governor's
Chair Program. YZ and WJW were supported by the U.S. Department of
Energy, Office of Science, Basic Energy Sciences, Division of Material
Science and Engineering.

# References
