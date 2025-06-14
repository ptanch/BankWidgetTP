import os
from unittest.mock import Mock, patch

from src.csv_excel_transactions import read_csv_transactions, read_excel_transactions


#  Tests for CSV
def test_read_csv_transactions_success():
    fake_df = Mock()
    expected = [{"id": 1, "amount": 100}]
    fake_df.to_dict.return_value = expected

    with patch("csv_excel_transactions.pd.read_csv", return_value=fake_df) as mock_read:
        result = read_csv_transactions("dummy/path.csv")

    expected_path = os.path.abspath("dummy/path.csv")
    mock_read.assert_called_once_with(expected_path, encoding="utf-8")
    fake_df.to_dict.assert_called_once_with(orient="records")
    assert result == expected


def test_read_csv_transactions_file_not_found(capsys):
    with patch("csv_excel_transactions.pd.read_csv", side_effect=FileNotFoundError()):
        result = read_csv_transactions("missing.csv")

    captured = capsys.readouterr()
    assert result == []
    assert "Файл не найден" in captured.out


def test_read_csv_transactions_generic_error(capsys):
    with patch("csv_excel_transactions.pd.read_csv", side_effect=ValueError("boom")):
        result = read_csv_transactions("bad.csv")

    captured = capsys.readouterr()
    assert result == []
    assert "Ошибка при чтении файла" in captured.out


#  Tests for Excel
def test_read_excel_transactions_success():
    fake_df = Mock()
    expected = [{"id": 2, "amount": 200}]
    fake_df.to_dict.return_value = expected

    with patch("src.csv_excel_transactions.pd.read_excel", return_value=fake_df) as mock_read:
        result = read_excel_transactions("dummy/path.xlsx")

    expected_path = os.path.abspath("dummy/path.xlsx")
    mock_read.assert_called_once_with(expected_path, engine="openpyxl")
    fake_df.to_dict.assert_called_once_with(orient="records")
    assert result == expected


def test_read_excel_transactions_file_not_found(capsys):
    with patch("csv_excel_transactions.pd.read_excel", side_effect=FileNotFoundError()):
        result = read_excel_transactions("missing.xlsx")

    captured = capsys.readouterr()
    assert result == []
    assert "Файл не найден" in captured.out


def test_read_excel_transactions_generic_error(capsys):
    with patch("csv_excel_transactions.pd.read_excel", side_effect=ValueError("boom")):
        result = read_excel_transactions("bad.xlsx")

    captured = capsys.readouterr()
    assert result == []
    assert "Ошибка при чтении файла" in captured.out
