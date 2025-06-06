import unittest
from unittest.mock import patch, mock_open
import json
from src.utils import read_transactions


class TestReadTransactions(unittest.TestCase):

    @patch("src.utils.os.path.isfile", return_value=True)
    @patch("src.utils.open", new_callable=mock_open, read_data=json.dumps([
        {"id": 1, "amount": 100}, {"id": 2, "amount": 200}
    ]))
    def test_valid_json_list_of_dicts(self, mock_file, mock_isfile):
        result = read_transactions("any_path.json")
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], dict)

    @patch("src.utils.os.path.isfile", return_value=False)
    def test_file_does_not_exist(self, mock_isfile):
        result = read_transactions("non_existing.json")
        self.assertEqual(result, [])

    @patch("src.utils.os.path.isfile", return_value=True)
    @patch("src.utils.open", new_callable=mock_open, read_data="INVALID JSON")
    def test_invalid_json(self, mock_file, mock_isfile):
        result = read_transactions("corrupted.json")
        self.assertEqual(result, [])

    @patch("src.utils.os.path.isfile", return_value=True)
    @patch("src.utils.open", new_callable=mock_open, read_data=json.dumps({"id": 1}))
    def test_json_not_a_list(self, mock_file, mock_isfile):
        result = read_transactions("notalist.json")
        self.assertEqual(result, [])

    @patch("src.utils.os.path.isfile", return_value=True)
    @patch("src.utils.open", new_callable=mock_open, read_data=json.dumps([1, 2, 3]))
    def test_json_list_not_dicts(self, mock_file, mock_isfile):
        result = read_transactions("list_of_non_dicts.json")
        self.assertEqual(result, [])


if __name__ == '__main__':
    unittest.main()
