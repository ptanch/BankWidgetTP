import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from unittest.mock import Mock, patch

from src.external_api import get_transaction_amount_rub


class TestGetTransactionAmountRub(unittest.TestCase):

    def test_transaction_in_rub(self):
        transaction = {'amount': 150, 'currency': 'RUB'}
        result = get_transaction_amount_rub(transaction)
        self.assertEqual(result, 150.0)

    @patch('src.external_api.requests.get')
    def test_transaction_in_usd(self, mock_get):
        # Подготовка фейкового ответа API
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": 9200.0}  # 100 USD = 9200 RUB
        mock_get.return_value = mock_response

        transaction = {'amount': 100, 'currency': 'USD'}
        result = get_transaction_amount_rub(transaction)
        self.assertEqual(result, 9200.0)

        # Проверка, что requests.get вызвался с нужными аргументами
        mock_get.assert_called_once()
        called_args = mock_get.call_args[1]  # Получаем kwargs
        self.assertEqual(called_args["params"]["from"], "USD")
        self.assertEqual(called_args["params"]["to"], "RUB")

    @patch('src.external_api.requests.get')
    def test_api_error(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_get.return_value = mock_response

        transaction = {'amount': 100, 'currency': 'USD'}
        with self.assertRaises(Exception) as context:
            get_transaction_amount_rub(transaction)

        self.assertIn("Ошибка при запросе к API", str(context.exception))

if __name__ == '__main__':
    unittest.main()