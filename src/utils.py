import json
import os


def read_transactions(file_path):
    """
    Function reads JSON-file with transaction info
    :param file_path: Путь к JSON-файлу.
    :return: Список словарей с транзакциями, либо пустой список при ошибке
    """
    if not os.path.isfile(file_path):
        return []

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if isinstance(data, list) and all(isinstance(item, dict) for item in data):
                return data
    except (json.JSONDecodeError, IOError):
        pass

    return []


if __name__ == "__main__":
    transactions = read_transactions('data/operations.json')
    print(transactions)
    print("Файл существует:", os.path.isfile('data/operations.json'))