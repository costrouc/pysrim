---
title: Automation of SRIM
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
affiliations:
  - name: "Department of Material Science and Engineering, University of Tennessee"
    index: 1
date: 18 April 2018
bibliography: paper.bib
---

# Summary

The behavior of ions traveling through a material is of great interest
to many fields. For instance radiation materials and ion beam
modification are most concered with the bulk of the material and
understanding the damage formation and evolution of defects along the
ion path [@was2016fundamentals]. Some of the imporant properties that
can be gleaned from investigating the initial damage from the ion
include: number of vacancies produced, energy deposited per unit
length, and average deposition distance. These properties enables
further simulations for multiscale modeling and to compute a common
radiation damage unit displacements per atom (DPA)
[@stoller2013use]. In other fields they are most concerned with the
ejection of materials near the surface due to incident ions with
techniques such as RBS, SIMS, and sputtering.

The interaction of ions with a material can be broken into two parts:
electronic and nuclear stopping. Electronic stopping is the energy
lost from the ion due to interacting with the electrons along its
path. While nuclear stopping is the energy lost due to collisision
between the ion and atoms within the material. The Stopping and Range
of Ions in Matter (SRIM) is a well known software in nuclear community
that allow the simulation via Monte Carlo of ions through a material
[@ziegler2010srim]. SRIM was originally written in 1985 and has had
updates on the electonic stopping powers since then. While the
executable SRIM is free to use for non-comercial use, the source code
is not available to the community. Without the source code we would
like to wrap and extend the capabilities of the software with
`pysrim`.

# Pysrim

`pysrim` is a python library for automating srim calculations,
analysis, and publication quality plotting. It is continuously
delivered, tested, and fully-documented module. In addition the
documentation includes several jupyter notebooks for getting started.

The first pain point that `pysrim` aims to solve is running the SRIM
calcualtion. SRIM has some well known limitations such as sporadically
crashing with large simulations and bad input values, only running on
Windows, and needing to be run interactively with user input. `pysrim`
solves this by having a consistent api compatible with windows, linux,
and OSX, having support for chunking large of calculations, and
recovering from SRIM crashes. All of these features allow SRIM to be
fully automated in python via `pysrim` with no user input needed.

After running these calculations SRIM will produce many output files
all of which are not convenient to parse and require complex regular
expressions. Traditionally research groups have copy and pasted
sections into excel for analysis. `pysrim` hopes to solve this by
providing parsers for all of the major output files. These output
files incluce:
[IONIZ.txt](https://pysrim.readthedocs.io/en/latest/source/srim.html#srim.output.Ioniz),
[VACANCY.txt](https://pysrim.readthedocs.io/en/latest/source/srim.html#srim.output.Vacancy),
[NOVAC.txt](https://pysrim.readthedocs.io/en/latest/source/srim.html#srim.output.NoVacancy),
[E2RECOIL.txt](https://pysrim.readthedocs.io/en/latest/source/srim.html#srim.output.EnergyToRecoils),
[PHONON.txt](https://pysrim.readthedocs.io/en/latest/source/srim.html#srim.output.Phonons),
[RANGE.txt](https://pysrim.readthedocs.io/en/latest/source/srim.html#srim.output.Range),
and
[COLLISON.txt](https://pysrim.readthedocs.io/en/latest/source/srim.html#srim.output.Collision). Once
the output file is parsed the data is in convenient numpy arrays. With
the results `pysrim` provides utilities for producing plots for damage
energy, ionization per unit depth, vacancies produced per unit depth,
and even complex plots that require all of the collisions
information. The flexibility of the parsed output files allows for
additional plots to be created by the user. This software has
currently been used for the SRIM calcualtions, analysis, and plotting
in two publications [@zhang2017coupled] [@zhang2014effect].

![Plots produced by `pysrim` of vacancies produced for ions traveling
through $SiC$ material. (top) $Si$ ion (bottom) $Ni$
ion](length-heatmap-log-cropped.png)

# Acknowledgements

CO acknowledges support from the ...

# References
