import os
import requests
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv('EXCHANGE_RATES_API_KEY')
API_URL = "https://api.apilayer.com/exchangerates_data/convert"


def get_transaction_amount_rub(transaction: dict) -> float:
    amount = transaction['amount']
    currency = transaction['currency']

    if currency == 'RUB':
        return float(amount)

    response = requests.get(API_URL, params={
        "from": currency,
        "to": "RUB",
        "amount": amount
    }, headers={
        "apikey": API_KEY
    })

    if response.status_code != 200:
        raise Exception(f"Ошибка при запросе к API: {response.status_code}, {response.text}")

    data = response.json()
    return float(data["result"])


if __name__ == "__main__":
    transaction1 = {'amount': 100, 'currency': 'USD'}
    transaction2 = {'amount': 100, 'currency': 'RUB'}

    print(get_transaction_amount_rub(transaction1))  # Конвертирует 100 USD в RUB
    print(get_transaction_amount_rub(transaction2))  # Вернёт 100.0
