import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


# tests for filter_by_currency
@pytest.fixture
def transactions_sample():
    return [
        {
            "id": 1,
            "operationAmount": {
                "amount": "100.00",
                "currency": {"name": "USD", "code": "USD"}
            },
        },
        {
            "id": 2,
            "operationAmount": {
                "amount": "200.00",
                "currency": {"name": "EUR", "code": "EUR"}
            },
        },
        {
            "id": 3,
            "operationAmount": {
                "amount": "300.00",
                "currency": {"name": "USD", "code": "USD"}
            },
        },
    ]


@pytest.mark.parametrize("currency_code,expected_ids", [
    ("USD", [1, 3]),
    ("EUR", [2]),
    ("RUB", []),
])
def test_filter_by_currency(transactions_sample, currency_code, expected_ids):
    result = filter_by_currency(transactions_sample, currency_code)
    result_ids = [t["id"] for t in result]
    assert result_ids == expected_ids


def test_filter_by_currency_empty_list():
    result = list(filter_by_currency([], "USD"))
    assert result == []


def test_filter_by_currency_no_matching_currency():
    transactions = [
        {
            "id": 10,
            "operationAmount": {
                "amount": "500.00",
                "currency": {"name": "JPY", "code": "JPY"}
            },
        }
    ]
    result = list(filter_by_currency(transactions, "USD"))
    assert result == []


# tests for transaction_descriptions
@pytest.fixture
def description_transactions():
    return [
        {"description": "Перевод организации"},
        {"description": "Оплата услуг"},
        {"description": "Снятие наличных"},
    ]


@pytest.mark.parametrize("expected", [
    ["Перевод организации", "Оплата услуг", "Снятие наличных"],
])
def test_transaction_descriptions_output(description_transactions, expected):
    result = list(transaction_descriptions(description_transactions))
    assert result == expected


def test_transaction_descriptions_empty():
    result = list(transaction_descriptions([]))
    assert result == []


# tests for card_number_generator
@pytest.mark.parametrize("start,end,expected", [
    (1, 3, [
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
        "0000 0000 0000 0003"
    ]),
    (9999, 10000, [
        "0000 0000 0000 9999",
        "0000 0000 0001 0000"
    ]),
])
def test_card_number_generator_range(start, end, expected):
    result = list(card_number_generator(start, end))
    assert result == expected


@pytest.mark.parametrize("number,expected", [
    (0, "0000 0000 0000 0000"),
    (1234567890123456, "1234 5678 9012 3456"),
])
def test_card_number_generator_format(number, expected):
    result = next(card_number_generator(number, number))
    assert result == expected


def test_card_number_generator_edge_and_end():
    gen = card_number_generator(9999999999999998, 9999999999999999)
    result = list(gen)
    assert result == [
        "9999 9999 9999 9998",
        "9999 9999 9999 9999"
    ]
