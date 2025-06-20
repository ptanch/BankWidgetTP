import os
from typing import Dict, List

from src.csv_excel_transactions import read_csv_transactions, read_excel_transactions
from src.generators import filter_by_currency
from src.processing import filter_by_state, sort_by_date
from src.search_transactions import process_bank_search
from src.utils import read_transactions
from src.widget import get_date, mask_account_card

AVAILABLE_STATUSES = {"EXECUTED", "CANCELED", "PENDING"}


def display_transactions(transactions: List[Dict]) -> None:
    """Печатает список транзакций в читаемом виде."""
    if not transactions:
        print("\nПрограмма: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print("\nПрограмма: Распечатываю итоговый список транзакций...\n")
    print(f"Всего банковских операций в выборке: {len(transactions)}\n")

    for tx in transactions:
        # 1. Дата + описание
        date_str = get_date(tx.get("date", ""))
        print(f"{date_str} {tx.get('description', '').strip()}")

        # 2. Откуда / куда (могут отсутствовать)
        from_to_parts = []
        if "from" in tx and tx["from"]:
            from_to_parts.append(mask_account_card(tx["from"]))
        if "to" in tx and tx["to"]:
            from_to_parts.append(mask_account_card(tx["to"]))
        if from_to_parts:
            print(" -> ".join(from_to_parts))

        # 3. Сумма + валюта
        amount = tx.get("operationAmount", {}).get("amount", "")
        code = tx.get("operationAmount", {}).get("currency", {}).get("code", "")
        if not amount:  # резервный вариант, вдруг другая структура
            amount = tx.get("amount", "")
            code = tx.get("currency", "")
        print(f"Сумма: {amount} {code}\n")


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
        file_path = os.path.join("data", "operations.json")
        transactions = read_transactions(file_path)

    elif choice == "2":
        print("Программа: Для обработки выбран CSV-файл.")
        file_path = os.path.join("data", "transactions.csv")
        transactions = read_csv_transactions(file_path)

    elif choice == "3":
        print("Программа: Для обработки выбран XLSX-файл.")
        file_path = os.path.join("data", "transactions_excel.xlsx")
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

    #  Фильтрация по ключевому слову в описании
    print("\nПрограмма: Отфильтровать список транзакций по определенному слову в описании? Да/Нет")
    desc_answer = input("Пользователь: ").strip().lower()

    if desc_answer == "да":
        keyword = input("Программа: Введите ключевое слово для фильтрации: ").strip()
        transactions = process_bank_search(transactions, keyword)
        print(f"Программа: Выполнен поиск по ключевому слову '{keyword}' в описаниях операций.")
    else:
        print("Программа: Фильтрация по описанию пропущена.")

    display_transactions(transactions)


if __name__ == "__main__":
    main()
