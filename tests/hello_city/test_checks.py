import pytest
from check import *

fails = (
    './fail_empty.py',
    './fail_output.py',
    './fail_syntax.py',
    './fail_varnames.py',
)
success = (
    './success.py',
    # './success2.py',
    '../../hello_city.py',
)


@pytest.mark.parametrize("script", success)
def test_success_scripts(script, test_data):
    # Must pass with all test_data combinations
    check_contains_code(script)
    check_syntax(script, test_data)
    check_variables(script)
    check_name(script, test_data)
    check_city(script, test_data)


@pytest.mark.parametrize("script", fails)
def test_fail_scripts(script, test_data):
    # Must fail (raise AssertionError) with all test_data combinations
    with pytest.raises(AssertionError):
        check_contains_code(script)
        check_syntax(script, test_data)
        check_variables(script)
        check_name(script, test_data)
        check_city(script, test_data)
