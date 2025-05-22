import os
import sys
from src.masks import get_mask_account, get_mask_card_number

import pytest
from typing import List, Any
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))


@pytest.fixture
def valid_card_numbers() -> List[str]:
    return ["1234567890123456", "9876543210987654", "0000001111112222"]


@pytest.fixture
def edge_case_card_numbers() -> List[str]:
    return [
        "",
        "123",
        "123456",
        "1234567890",
        "12345678901234567890",
        "1234abcd5678efgh",
    ]


@pytest.mark.parametrize(
    "card_number,expected",
    [
        ("1234567890123456", "1234 56** **** 3456"),
        ("9876543210987654", "9876 54** **** 7654"),
        ("0000001111112222", "0000 00** **** 2222"),
    ],
)
def test_masking_valid_cards(card_number: str, expected: str) -> None:
    assert get_mask_card_number(card_number) == expected


def test_valid_fixture_cards(valid_card_numbers: List[str]) -> None:
    for card_number in valid_card_numbers:
        result = get_mask_card_number(card_number)

        assert len(result.replace(" ", "")) == len(card_number)

        unmasked = result.replace(" ", "")
        assert unmasked[6:12] == "******"

        blocks = result.split()
        assert all(len(block) == 4 for block in blocks)


@pytest.mark.parametrize(
    "invalid_input,expected_exception",
    [
        ("123", ValueError),
        ("1234567890", ValueError),
        ("abcd5678efgh1234", ValueError),
        (None, TypeError),
        (1234567890123456, TypeError),
    ],
)
def test_invalid_inputs_raise_exceptions(invalid_input: Any, expected_exception: type[Exception]) -> None:
    with pytest.raises(expected_exception):
        get_mask_card_number(invalid_input)


@pytest.mark.parametrize(
    "account_number, expected",
    [
        ("1234567890", "**7890"),
        ("00001234", "**1234"),
        ("99990000", "**0000"),
    ],
)
def test_mask_account_correct(account_number: str, expected: str) -> None:
    result = get_mask_account(account_number)
    assert result == expected


@pytest.mark.parametrize("account_number", ["0000", "1234", "9999"])
def test_mask_account_min_length(account_number: str) -> None:
    result = get_mask_account(account_number)
    assert result == "**" + account_number[-4:]


@pytest.mark.parametrize("invalid_account_number", ["", "1", "12", "123"])
def test_mask_account_too_short(invalid_account_number: str) -> None:
    with pytest.raises(ValueError):
        get_mask_account(invalid_account_number)


@pytest.mark.parametrize("invalid_type_input", [None, 12345678, ["12345678"], {"account": "12345678"}])
def test_mask_account_invalid_type(invalid_type_input: Any) -> None:
    with pytest.raises(TypeError):
        get_mask_account(invalid_type_input)
