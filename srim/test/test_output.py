import os

import pytest

from srim.output import (
    Ioniz, NoVacancy, Vacancy, EnergyToRecoils, Phonons, Range, Results
)

TESTDATA_DIRECTORY = os.path.join(os.path.dirname(__file__), 'data')


@pytest.mark.parametrize("directory", [("1"), ("2"), ("3"), ("4")])
def test_ioniz_init(directory):
    ion = Ioniz(os.path.join(TESTDATA_DIRECTORY, directory))
    assert ion.depth.shape == (100,)
    assert ion.ions.shape == (100,)
    assert ion.recoils.shape == (100,)

@pytest.mark.parametrize("directory", [("1"), ("2"), ("3"), ("4")])
def test_phonons_init(directory):
    phonons = Phonons(os.path.join(TESTDATA_DIRECTORY, directory))
    assert phonons.depth.shape == (100,)
    assert phonons.ions.shape == (100,)
    assert phonons.recoils.shape == (100,)

@pytest.mark.parametrize("directory", [("1"), ("2"), ("3"), ("4")])
def test_vacancy_init(directory):
    vac = Vacancy(os.path.join(TESTDATA_DIRECTORY, directory))
    assert vac.depth.shape == (100,)

@pytest.mark.parametrize("directory", [("1"), ("2"), ("3"), ("4")])
def test_range_init(directory):
    range = Range(os.path.join(TESTDATA_DIRECTORY, directory))
    assert range.depth.shape == (100,)

@pytest.mark.parametrize("directory", [("1"), ("2"), ("3")])
def test_novacancy_init_full_calculation(directory):
    novac = NoVacancy(os.path.join(TESTDATA_DIRECTORY, directory))
    assert novac.depth.shape == (100,)
    assert novac.number.shape == (100,)

def test_novacancy_init_kp_calculation():
    with pytest.raises(ValueError) as excinfo:
        NoVacancy(os.path.join(TESTDATA_DIRECTORY, '4'))
    assert excinfo.value.args[0] == 'NOVAC has no data for KP calculations'
    
@pytest.mark.parametrize("directory", [("1"), ("2"), ("3"), ("4")])
def test_energytorecoils_init(directory):
    etorec = EnergyToRecoils(os.path.join(TESTDATA_DIRECTORY, directory))
    assert etorec.depth.shape == (100,)

@pytest.mark.parametrize("directory", [("1"), ("2"), ("3")])
def test_results_init_full(directory):
    results = Results(os.path.join(TESTDATA_DIRECTORY, directory))
    assert isinstance(results.ioniz, Ioniz)
    assert isinstance(results.vacancy, Vacancy)
    assert isinstance(results.novac, NoVacancy)
    assert isinstance(results.etorecoils, EnergyToRecoils)
    assert isinstance(results.phonons, Phonons)
    assert isinstance(results.range, Range)

def test_resuls_init_kp_calculation():
    results = Results(os.path.join(TESTDATA_DIRECTORY, '4'))
    assert isinstance(results.ioniz, Ioniz)
    assert isinstance(results.vacancy, Vacancy)
    assert results.novac == None
    assert isinstance(results.etorecoils, EnergyToRecoils)
    assert isinstance(results.phonons, Phonons)
    assert isinstance(results.range, Range)

