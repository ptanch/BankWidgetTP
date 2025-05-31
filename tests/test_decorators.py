import os
import pytest
from src.decorators import log


#  test for console output
def test_success_console_log(capsys):
    @log()
    def func_add (x, y):
        return x + y

    result = func_add(2, 3)
    captured = capsys.readouterr()
    assert result == 5
    assert "func_add ok" in captured.out


def test_error_console_log(capsys):
    @log()
    def fail_func(a, b):
        return a / b

    with pytest.raises(ZeroDivisionError):
        fail_func(1, 0)

    captured = capsys.readouterr()
    assert "fail_func error: ZeroDivisionError. Inputs: (1, 0), {}" in captured.out


#  tests with logging in file
def test_success_file_log(tmp_path):
    log_file = tmp_path / "log.txt"

    @log(filename=str(log_file))
    def func_multiply(x, y):
        return x * y

    result = func_multiply(4, 5)
    assert result == 20

    content = log_file.read_text()
    assert "func_multiply" in content

def test_error_file_log(tmp_path):
    log_file = tmp_path / "log.txt"

    @log(filename=str(log_file))
    def fail_func(a, b):
        return a / b

    with pytest.raises(ZeroDivisionError):
        fail_func(10, 0)

    content = log_file.read_text()
    assert "fail_func error: ZeroDivisionError. Inputs: (10, 0), {}" in content
