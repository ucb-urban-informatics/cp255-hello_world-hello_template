import pytest
import ast
import subprocess

"""
contains code
no syntax error
variables start with lowercase
prints expected values for each function
"""


@pytest.fixture(params=[
    ('Alex', 'Tokyo', 'Hello, Alex!', 'Hope you visit Tokyo soon!'),
    ('Amari', 'Nairobi', 'Hello, Amari!', 'Hope you visit Nairobi soon!'),
    ('Avery', 'Reykjavík', 'Hello, Avery!', 'Hope you visit Reykjavík soon!'),
    ('Devika', 'Lisbon', 'Hello, Devika!', 'Hope you visit Lisbon soon!'),
    ('Ezra', 'Bengaluru', 'Hello, Ezra!', 'Hope you visit Bengaluru soon!')
])
def test_data(request):
    return request.param


def call(
        script: str,
        test_data: tuple[str, str, str, str],
        **kwargs,
):
    """
    Calls the script with the given test data.
    """
    person, city, line1, line2 = test_data
    args = ['python', script]
    inp = f'{person}\n{city}\n'
    result = subprocess.run(
        args,
        input=inp,
        text=True,
        capture_output=True,
        **kwargs
    )
    return result

def check_contains_code(
        script: str,
):
    """
    checks:
        contains code
    """
    with open(script, 'r', encoding='utf-8') as f:
        source = f.read()

    msg = '❌ No code found in script.'
    assert source.strip(), msg


def check_syntax(
        script: str,
        test_data: tuple[str, str, str, str],
):
    """
    checks:
        no syntax error
    """
    result = call(script, test_data)
    msg = f'❌ SyntaxError encountered:\n {result.stderr}'
    assert 'SyntaxError' not in result.stderr, msg


def check_variables(
        script: str,
):
    """
    checks:
        variables do not start with uppercase
    """
    with open(script, 'r', encoding='utf-8') as f:
        source = f.read()

    tree = ast.parse(source)

    for node in ast.walk(tree):
        # Check any variable assigned (global or local)
        if (
                isinstance(node, ast.Name)
                and isinstance(node.ctx, ast.Store)
        ):
            msg = f'Variable "{node.id}" starts with uppercase.'
            assert not (
                    node.id
                    and node.id[0].isupper()
            ), msg

        # Check function parameters
        if isinstance(node, ast.FunctionDef):
            for arg in node.args.args:
                msg = f'Parameter "{arg.arg}" starts with uppercase.'
                assert not (
                        arg.arg
                        and arg.arg[0].isupper()
                ), msg



def check_name(
        script: str,
        test_data: tuple[str, str, str, str],
):
    person, city, line1, line2 = test_data
    result = call(script, test_data)
    output = result.stdout.strip()

    assert output, "Output must not be empty."
    msg = (
        f'❌ Expected substring:\n {line1}\n'
        f'in the output, but it was not found.\n'
        f'Output:\n{output}'
    )
    assert line1 in output, msg


def check_city(
        script: str,
        test_data: tuple[str, str, str, str],
):
    person, city, line1, line2 = test_data
    result = call(script, test_data)
    output = result.stdout.strip()

    assert output, "Output must not be empty."
    msg = (
        f'❌ Expected substring:\n {line2}\n'
        f'in the output, but it was not found.\n'
        f'Output:\n{output}'
    )
    assert line2 in output, msg
