import os

import pytest

from srim.output import (
    Ioniz, NoVacancy, Vacancy, EnergyToRecoils, Phonons, Range,
    Results, SRResults
)

TESTDATA_DIRECTORY = 'test_files'


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

def test_results_srim_calcluation():
    results = SRResults(os.path.join(TESTDATA_DIRECTORY, 'SRIM'))
    assert results.ion == {'A1': 131.293, 'Z1': 54, 'name': 'Xenon'}
    assert results.data.shape == (6, 159)
    assert results.units == "MeV/(mg/cm2)"
    assert results.target == {
        'density atoms/cm3': 9.6421e+22,
        'density g/cm3': 3.21,
        'target composition': {
            'C': [6, 50.0, 29.95],
            'Si': [14, 50.0, 70.05]
        }
    }
