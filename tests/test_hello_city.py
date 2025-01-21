from .hello_city.check import *
import pytest

path = 'hello_city.py',


@pytest.mark.parametrize("script", path)
def test_script_contains_code(script):
    check_contains_code(script)


@pytest.mark.parametrize("script", path)
def test_script_syntax(script, test_data):
    check_syntax(script, test_data)


@pytest.mark.parametrize("script", path)
def test_variables(script):
    check_variables(script)


@pytest.mark.parametrize("script", path)
def test_name(script, test_data):
    check_name(script, test_data)


@pytest.mark.parametrize("script", path)
def test_city(script, test_data):
    check_city(script, test_data)


