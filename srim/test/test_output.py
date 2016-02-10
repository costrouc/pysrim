import os

import pytest

from srim.output import Ioniz


TESTDATA_DIRECTORY = os.path.join(os.path.dirname(__file__), 'data')


def test_ioniz_init():
    Ioniz(TESTDATA_DIRECTORY)
