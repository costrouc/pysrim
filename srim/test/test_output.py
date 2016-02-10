import os

import pytest

from srim.output import (
    Ioniz, NoVacancy, Vacancy, EnergyToRecoils
)

TESTDATA_DIRECTORY = os.path.join(os.path.dirname(__file__), 'data')


@pytest.mark.parametrize("input_file", [("1"), ("2"), ("3")])
def test_ioniz_init(input_file):
    Ioniz(os.path.join(TESTDATA_DIRECTORY, input_file))


@pytest.mark.parametrize("input_file", [("1"), ("2"), ("3")])
def test_vacancy_init(input_file):
    Vacancy(os.path.join(TESTDATA_DIRECTORY, input_file))


@pytest.mark.parametrize("input_file", [("1"), ("2"), ("3")])
def test_novacancy_init(input_file):
    NoVacancy(os.path.join(TESTDATA_DIRECTORY, input_file))


@pytest.mark.parametrize("input_file", [("1"), ("2"), ("3")])
def test_energytorecoils_init(input_file):
    EnergyToRecoils(os.path.join(TESTDATA_DIRECTORY, input_file))
