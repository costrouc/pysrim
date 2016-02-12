import os

import pytest

from srim.output import (
    Ioniz, NoVacancy, Vacancy, EnergyToRecoils, Phonons, Range
)

TESTDATA_DIRECTORY = os.path.join(os.path.dirname(__file__), 'data')


@pytest.mark.parametrize("input_file", [("1"), ("2"), ("3")])
def test_ioniz_init(input_file):
    ion = Ioniz(os.path.join(TESTDATA_DIRECTORY, input_file))
    assert ion.depth.shape == (100,)
    assert ion.ions.shape == (100,)
    assert ion.recoils.shape == (100,)

@pytest.mark.parametrize("input_file", [("1"), ("2"), ("3")])
def test_phonons_init(input_file):
    phonons = Phonons(os.path.join(TESTDATA_DIRECTORY, input_file))
    assert phonons.depth.shape == (100,)
    assert phonons.ions.shape == (100,)
    assert phonons.recoils.shape == (100,)

@pytest.mark.parametrize("input_file", [("1"), ("2"), ("3")])
def test_vacancy_init(input_file):
    vac = Vacancy(os.path.join(TESTDATA_DIRECTORY, input_file))
    assert vac.depth.shape == (100,)

@pytest.mark.parametrize("input_file", [("1"), ("2"), ("3")])
def test_range_init(input_file):
    range = Range(os.path.join(TESTDATA_DIRECTORY, input_file))
    assert range.depth.shape == (100,)

@pytest.mark.parametrize("input_file", [("1"), ("2"), ("3")])
def test_novacancy_init(input_file):
    novac = NoVacancy(os.path.join(TESTDATA_DIRECTORY, input_file))
    assert novac.depth.shape == (100,)
    assert novac.number.shape == (100,)

@pytest.mark.parametrize("input_file", [("1"), ("2"), ("3")])
def test_energytorecoils_init(input_file):
    etorec = EnergyToRecoils(os.path.join(TESTDATA_DIRECTORY, input_file))
    assert etorec.depth.shape == (100,)
