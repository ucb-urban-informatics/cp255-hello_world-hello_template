import pytest
from .hello_city.check import *

path = '.hello.py',


@pytest.mark.points(1)
@pytest.mark.parametrize("script", path)
def test_prints_hello_world(script):
    check_contains_code(script)
    args = ['python', script]
    result = subprocess.run(args, text=True, capture_output=True)
    assert result.returncode == 0, f'❌ Script did not run successfully. {result.stderr}'
    assert result.stdout.strip(), '❌ Script did not print anything.'
    assert result.stdout.strip() == 'Hello, World!', '❌ Script did not print "Hello, World!"'
