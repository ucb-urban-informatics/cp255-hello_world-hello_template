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


def check_output(
        script: str,
        test_data: tuple[str, str, str, str],
):
    """
    Tests:
        no syntax error
        prints expected values for each function
    """
    person, city, line1, line2 = test_data
    args = ['python', script]
    inp = f'{person}\n{city}\n'
    result = subprocess.run(
        args,
        input=inp,
        text=True,
        capture_output=True
    )
    # no syntax error
    msg = f'❌ SyntaxError encountered:\n {result.stderr}'
    assert 'SyntaxError' not in result.stderr, msg
    assert result.returncode == 0, f"Non-zero return code: {result.returncode}"
    lines = (
        result.stdout
        .strip()
        .split("\n")
    )

    assert len(lines) >= 2, "Output must have at least two lines"
    msg = (
        f'❌ Expected first line: {line1}, but got: {lines[-2]}. '
        f'💡 Please ensure your printouts correctly format and order the output messages.'
    )
    assert lines[-2] == line1, msg
    msg = (
        f'❌ Expected second line: {line2}, but got: {lines[-1]}. '
        f'💡 Please ensure your printouts correctly format and order the output messages.'
    )
    assert lines[-1] == line2, msg

def check_variables(
        script: str,
):
    """
    Tests:
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

