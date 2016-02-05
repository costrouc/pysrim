import pytest

from srim.core.elementdb import ElementDB

# ElementDB size
def test_db_size():
    assert len(ElementDB._db) == 112


# ElementDB Lookups
def test_lookup_symbol():
    element = ElementDB._lookup_symbol('Fe')
    assert element['symbol'] == 'Fe'
    assert element['name'] == 'Iron'


def test_lookup_invalid_symbol():
    with pytest.raises(KeyError):
        ElementDB._lookup_symbol('Zx')


def test_lookup_name():
    element = ElementDB._lookup_name('Aluminium')
    assert element['symbol'] == 'Al'
    assert element['name'] == 'Aluminium'


def test_lookup_invalid_name():
    with pytest.raises(KeyError):
        ElementDB._lookup_name('Macium') # My gf's name


def test_lookup_atomic_number():
    element = ElementDB._lookup_atomic_number(100)
    assert element['symbol'] == 'Fm'
    assert element['name'] == 'Fermium'


def test_lookup_invalid_atomic_number_negative():
    with pytest.raises(IndexError):
        ElementDB._lookup_atomic_number(-1)


def test_lookup_invalid_atomic_number_large():
    with pytest.raises(IndexError):
        ElementDB._lookup_atomic_number(130)


# Test lookup correct function
def test_lookup_call_symbol(mocker):
    mocker.patch('srim.core.elementdb.ElementDB._lookup_symbol')
    ElementDB.lookup('Au')
    ElementDB._lookup_symbol.assert_called_once_with('Au')


def test_lookup_call_name(mocker):
    mocker.patch('srim.core.elementdb.ElementDB._lookup_name')
    ElementDB.lookup('Gold')
    ElementDB._lookup_name.assert_called_once_with('Gold')


def test_lookup_call_atomic_number(mocker):
    mocker.patch('srim.core.elementdb.ElementDB._lookup_atomic_number')
    ElementDB.lookup(100)
    ElementDB._lookup_atomic_number.assert_called_once_with(100)
