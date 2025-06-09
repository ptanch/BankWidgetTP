import logging
import json
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, 'logs')
os.makedirs(LOG_DIR, exist_ok=True)
LOG_PATH = os.path.join(BASE_DIR, 'logs', 'info.log')


logger = logging.getLogger('utils')
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(LOG_PATH, mode='w', encoding='utf-8')
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)


#  Избежание дублирования логов
if not logger.handlers:
    logger.addHandler(file_handler)


def read_transactions(file_path):
    """
    Function reads JSON-file with transaction info
    :param file_path: Path to JSON-file.
    :return: List of dictionaries with transactions, or empty list on error
    """
    abs_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'operations.json')
    abs_path = os.path.abspath(abs_path)

    logger.debug(f"Попытка чтения файла по пути: {abs_path}")

    if not os.path.isfile(abs_path):
        logger.error(f"Файл не найден: {abs_path}")
        return []

    try:
        with open(abs_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if isinstance(data, list) and all(isinstance(item, dict) for item in data):
                logger.debug(f"Успешно прочитаны и проверены данные транзакции из {abs_path}")
                return data
            else:
                logger.error(f"Файл не содержит список словарей: {abs_path}")
    except (json.JSONDecodeError, IOError) as e:
        logger.error(f"Ошибка при чтении файла {abs_path}: {e}")
    except IOError as e:
        logger.error(f"Ошибка ввода-вывода при чтении файла {abs_path}: {e}")

    return []


if __name__ == "__main__":  # pragma: no cover
    transactions = read_transactions('не используется')
    print(transactions)
