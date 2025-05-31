MAX_CARD_NUMBER = 9999999999999999


def filter_by_currency(transactions, currency_code):
    """Filters transactions and returns the iterator"""

    return (
        transaction
        for transaction in transactions
        if transaction.get("operationAmount", {}).get("currency", {}).get("code") == currency_code
    )


def transaction_descriptions(transactions):
    """Getting description of operations"""

    for transaction in transactions:
        yield transaction.get("description", "")


def card_number_generator(start, end):
    """Generation of card number"""

    if start < 0 or end > MAX_CARD_NUMBER:
        raise ValueError("Card number must be in range 0000000000000000 to 9999999999999999")
    for number in range(start, end + 1):
        formatted = f"{number:016d}"
        yield f"{formatted[:4]} {formatted[4:8]} {formatted[8:12]} {formatted[12:]}"


if __name__ == "__main__":  # pragma: no cover
    transactions = [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
        {
            "id": 873106923,
            "state": "CANCELED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {"amount": "1234.56", "currency": {"name": "EUR", "code": "EUR"}},
            "description": "Оплата услуг",
            "from": "Счет 12345678901234567890",
            "to": "Счет 09876543210987654321",
        },
    ]

    usd_transactions = filter_by_currency(transactions, "USD")

    for _ in range(2):
        print(next(usd_transactions))

    transactions = [
        {"description": "Перевод организации"},
        {"description": "Перевод со счета на счет"},
        {"description": "Перевод со счета на счет"},
        {"description": "Перевод с карты на карту"},
        {"description": "Перевод организации"},
   ]

    descriptions = transaction_descriptions(transactions)

    for _ in range(5):
        print(next(descriptions))

    for card_number in card_number_generator(1, 5):
        print(card_number)
