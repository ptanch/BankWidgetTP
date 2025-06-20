import os

import pandas as pd


def read_csv_transactions(file_path):
    """
    Function reads CSV-file with transactions info
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


def read_excel_transactions(excel_file_path):
    """
    Functions reads Excel-file with transactions info
    :param excel_file_path: Path to Excel-file
    :return: List of dictionaries with transactions
    """

    abs_path = os.path.abspath(excel_file_path)

    try:
        df = pd.read_excel(abs_path, engine='openpyxl', dtype=str)
        df = df.fillna("")
        return df.to_dict(orient='records')
    except FileNotFoundError:
        print(f"Файл не найден: {abs_path}")
        return []
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return []


if __name__ == "__main__":  # pragma: no cover
    file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'transactions.csv')
    transactions = read_csv_transactions(file_path)
    print(f"Всего операций в CSV: {len(transactions)}")
    print(transactions[:3])

    excel_file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'transactions_excel.xlsx')
    transactions_excel = read_excel_transactions(excel_file_path)
    print(f"Всего операций в Excel: {len(transactions_excel)}")
    print(transactions_excel[:3])
