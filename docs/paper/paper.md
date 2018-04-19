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
    affiliation: "2, 1"
  - name: William Weber
    orcid: 0000-0000-0000-0000
    affiliation: "1, 2"
affiliations:
  - name: "Department of Material Science and Engineering, University of Tennessee"
    index: 1
  - name: "Materials Science and Technology Division, Oak Ridge National Laboratory"
    index: 2
date: 18 April 2018
bibliography: paper.bib
---

# Summary

The behavior of ions traveling through a material is of great interest
to many fields. For instance nuclear materials and ion beam
modification are most concerned with the bulk of the material and
understanding the damage formation and evolution of defects along the
ion path [@was2016fundamentals]. Some of the important properties that
can be gleaned from investigating the initial damage from the ion
include: number of vacancies produced, energy deposited per unit
length, track diameter, and implantation profile. These properties
enable further simulations and allow computing a common radiation
damage unit, displacements per atom (DPA), which can be used to
compare experiments [@backman2013molecular]
[@stoller2013use]. Additionally the ejection of materials near the
surface due to incident ions is important to techniques such as RBS,
SIMS, and sputtering [@vickerman2011surface]. The interaction of ions
within a material can be broken into two parts: electronic and nuclear
stopping. Electronic stopping is the energy lost from the ion due to
inelastic collisions with electrons along its path. Nuclear stopping
is the energy lost due to elastic collisions between the ion and
atomic nuclei within the material.

The Stopping and Range of Ions in Matter (SRIM) is a well known
software in the nuclear community that allows the simulation, via
Monte Carlo, of ions through a material by modeling the energy
transfer through electronic and nuclear stopping
[@ziegler2010srim]. SRIM was originally developed in 1985 and has had
numerous updates on the electronic stopping powers since then with the
nuclear stopping well explained by the ZBL potential
[@ziegler1988stopping]. The executable SRIM is free to use for
non-commercial use but the source code is not available to the
community despite requests. While SRIM is a scientifically accurate
code it does not get updated frequently and has many bugs from a
usability standpoint.

# Pysrim

`pysrim` is a python library for automating srim calculations,
analysis, and for publication quality plotting. It is a continuously
delivered, tested, and fully-documented module. In addition, the
documentation includes several jupyter notebooks for getting started.

The first pain point that `pysrim` aims to solve is running the SRIM
calculation. SRIM has some well known limitations such as crashing
with large simulations and bad input values, only running on Windows,
and needing to be run interactively with user input. `pysrim` solves
this by having an api compatible with windows, linux, and OS X, having
support for chunking of large calculations, and recovering from SRIM
crashes. All of these features allow SRIM to be fully automated via
`pysrim`.

After running these calculations SRIM will produce many output files
all of which are not convenient to parse. Traditionally research
groups have copy and pasted sections into excel for analysis. `pysrim`
hopes to solve this by providing parsers for all the major output
files. These output files include:
[IONIZ.txt](https://pysrim.readthedocs.io/en/latest/source/srim.html#srim.output.Ioniz),
[VACANCY.txt](https://pysrim.readthedocs.io/en/latest/source/srim.html#srim.output.Vacancy),
[NOVAC.txt](https://pysrim.readthedocs.io/en/latest/source/srim.html#srim.output.NoVacancy),
[E2RECOIL.txt](https://pysrim.readthedocs.io/en/latest/source/srim.html#srim.output.EnergyToRecoils),
[PHONON.txt](https://pysrim.readthedocs.io/en/latest/source/srim.html#srim.output.Phonons),
[RANGE.txt](https://pysrim.readthedocs.io/en/latest/source/srim.html#srim.output.Range),
and
[COLLISON.txt](https://pysrim.readthedocs.io/en/latest/source/srim.html#srim.output.Collision). Once
the output file is parsed the data is available in `numpy` arrays. From
here the user is free to create plots of interesting relationships in
their data. `pysrim` additionally provides plotting utilities for
producing figures commonly needed in nuclear materials. This software
has been used for the SRIM calculations, analysis, and plotting in two
publications [@zhang2017coupled] [@zhang2014effect].

![Plots produced by `pysrim` of vacancies for ions traveling through
$SiC$ material. (top) $Si$ ion (bottom) $Ni$
ion](length-heatmap-log-cropped.png)

# Acknowledgements

CO acknowledges support from the ...

# References
