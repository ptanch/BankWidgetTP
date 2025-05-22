import pytest

from src.widget import get_date, mask_account_card


@pytest.fixture
def valid_bank_data() -> dict[str, str]:
    return {
        "card": "Оплата с карты 1234567812345678 прошла успешно",
        "account": "Перевод на Счет 40817810099910004312 выполнен",
        "mixed": "Карта 4321432143214321 и Счет 40817810012345678901 в одной строке",
    }


@pytest.fixture
def invalid_bank_data() -> list[str]:
    return [
        "Счет 123456789012345",  # слишком короткий
        "Номер карты 12345678901234",  # слишком короткий
        "Карта ABCD1234EFGH5678",  # нечисловые символы
        "",  # пустая строка
        "Просто текст без номеров",  # нет номеров
    ]


@pytest.mark.parametrize(
    "input_text,expected",
    [
        ("Счет 40817810099910004312", "Счет **4312"),
        ("Оплата с карты 1234567812345678", "Оплата с карты 1234 56** **** 5678"),
        ("Карта 4321432143214321 и Счет 40817810012345678901", "Карта 4321 43** **** 4321 и Счет **8901"),
    ],
)
def test_masking_valid_cases(input_text: str, expected: str) -> None:
    result = mask_account_card(input_text)
    assert expected in result


@pytest.mark.parametrize(
    "invalid_input",
    ["Счет 123456789012345", "Номер карты 12345678901234", "Карта ABCD1234EFGH5678", "", "Просто текст без номеров"],
)
def test_masking_invalid_cases(invalid_input: str) -> None:
    result = mask_account_card(invalid_input)
    # В случае нераспознавания, результат должен остаться таким же
    assert result == invalid_input


def test_masking_from_fixture(valid_bank_data: dict[str, str]) -> None:
    result_card = mask_account_card(valid_bank_data["card"])
    assert "1234 56** **** 5678" in result_card

    result_account = mask_account_card(valid_bank_data["account"])
    assert "Счет **4312" in result_account

    result_mixed = mask_account_card(valid_bank_data["mixed"])
    assert "4321 43** **** 4321" in result_mixed
    assert "Счет **8901" in result_mixed


@pytest.mark.parametrize(
    "full_date,expected",
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("1999-12-01T00:00:00.000000", "01.12.1999"),
        ("2025-01-09T12:59:59.999999", "09.01.2025"),
    ],
)
def test_get_date_valid(full_date: str, expected: str) -> None:
    assert get_date(full_date) == expected


@pytest.mark.parametrize(
    "full_date, expected",
    [
        ("2024-03-11", "11.03.2024"),  # валидный ISO без времени
        ("20240311T022618", "11.03.2024"),  # валидный ISO без дефисов
        ("11.03.2024", "Некорректная дата"),  # не ISO формат
        ("", "Некорректная дата"),  # пустая строка
        ("текст вместо даты", "Некорректная дата"),  # произвольный текст
    ],
)
def test_get_date_various_inputs(full_date: str, expected: str) -> None:
    assert get_date(full_date) == expected
