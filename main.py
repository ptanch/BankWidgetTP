import os
from src.utils import read_transactions
from src.csv_excel_transactions import read_csv_transactions, read_excel_transactions
from src.processing import filter_by_state, sort_by_date
from src.generators import filter_by_currency


AVAILABLE_STATUSES = {"EXECUTED", "CANCELED", "PENDING"}


def main():
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input("Пользователь: ").strip()

    transactions = []

    if choice == "1":
        print("Программа: Для обработки выбран JSON-файл.")
        file_path = input(
            "Введите путь к JSON-файлу (по умолчанию: operations.json): ").strip() or "operations.json"
        transactions = read_transactions(file_path)

    elif choice == "2":
        print("Программа: Для обработки выбран CSV-файл.")
        file_path = input("Введите путь к CSV-файлу (по умолчанию: transactions.csv): ").strip() or "transactions.csv"
        transactions = read_csv_transactions(file_path)

    elif choice == "3":
        print("Программа: Для обработки выбран XLSX-файл.")
        file_path = input(
            "Введите путь к Excel-файлу (по умолчанию: transactions_excel.xlsx): ").strip() or "transactions_excel.xlsx"
        transactions = read_excel_transactions(file_path)

    else:
        print("Программа: Некорректный выбор. Пожалуйста, запустите программу снова.")
        return

    # Проверка, что данные загружены
    if not transactions:
        print("Программа: Не удалось загрузить данные. Завершение работы.")
        return

    while True:
        print("\nПрограмма: Введите статус, по которому необходимо выполнить фильтрацию.")
        print("Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING")
        user_status = input("Пользователь: ").strip().upper()

        if user_status in AVAILABLE_STATUSES:
            transactions = filter_by_state(transactions, user_status)
            print(f'Программа: Операции отфильтрованы по статусу "{user_status}"')
            break
        else:
            print(f'Программа: Статус операции "{user_status}" недоступен.')

    #  Сортировка по дате
    print("\nПрограмма: Отсортировать операции по дате? Да/Нет")
    sort_answer = input("Пользователь: ").strip().lower()

    if sort_answer == "да":
        print("\nПрограмма: Отсортировать по возрастанию или по убыванию?")
        order = input("Пользователь: ").strip().lower()

        if "возрастан" in order:
            transactions = sort_by_date(transactions, descending=False)
        else:
            transactions = sort_by_date(transactions, descending=True)

        print("Программа: Операции отсортированы по дате.")
    else:
        print("Программа: Сортировка по дате пропущена.")

    #  Фильтрация по валюте
    print("\nПрограмма: Выводить только рублевые транзакции? Да/Нет")
    currency_answer = input("Пользователь: ").strip().lower()

    if currency_answer == "да":
        transactions = list(filter_by_currency(transactions, "RUB"))
        print("Программа: Отобраны только транзакции в рублях.")
    else:
        print("Программа: Фильтрация по валюте пропущена.")
