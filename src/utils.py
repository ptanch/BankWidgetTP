import json
import os


def read_transactions(file_path):
    """
    Function reads JSON-file with transaction info
    :param file_path: Path to JSON-file.
    :return: List of dictionaries with transactions, or empty list on error
    """
    abs_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'operations.json')
    abs_path = os.path.abspath(abs_path)

    print("Абсолютный путь к файлу:", abs_path)
    if not os.path.isfile(abs_path):
        print("Файл не найден.")
        return []

    try:
        with open(abs_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if isinstance(data, list) and all(isinstance(item, dict) for item in data):
                return data
            else:
                print("Файл не содержит список словарей.")
    except (json.JSONDecodeError, IOError) as e:
        print("Ошибка при чтении файла:", e)

    return []


if __name__ == "__main__":
    transactions = read_transactions('не используется')
    print(transactions)