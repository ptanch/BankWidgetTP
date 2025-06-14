import os
import pandas as pd


def read_csv_transactions(file_path):
    """
    Function reads csv-file with transaction info
    :param file_path: Path to CSV-file
    :return: List of dictionaries with transactions
    """

    abs_path = os.path.abspath(file_path)

    try:
        df = pd.read_csv(abs_path, encoding='utf-8')
        transactions = df.to_dict(orient='records')
        return transactions
    except FileNotFoundError:
        print(f"Файл не найден: {abs_path}")
        return []
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return []


if __name__ == "__main__":
    file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'transactions.csv')
    transactions = read_csv_transactions(file_path)
    print(f"Всего операций: {len(transactions)}")
    print(transactions[:3])
