import re
from typing import Dict, List


def process_bank_search(data: List[Dict], search: str) -> List[Dict]:
    """Function for search in the list of operation dictionaries for a given string"""

    #  Компиляция регулярного выражения для поиска (регистр игнорируется)
    pattern = re.compile(re.escape(search), re.IGNORECASE)

    #  Фильтрация списка, выбираем только те словари, в которых описание содержит искомую строку
    result = [item for item in data if 'description' in item and pattern.search(item['description'])]

    return result


if __name__ == "__main__":  # pragma: no cover
    transactions = [
        {'id': 1, 'amount': 100, 'description': 'Оплата мобильной связи'},
        {'id': 2, 'amount': 250, 'description': 'Покупка в супермаркете'},
        {'id': 3, 'amount': 500, 'description': 'Перевод другу'},
        {'id': 4, 'amount': 120, 'description': 'Связь и интернет'},
    ]

    search_query = 'связи'

    matched = process_bank_search(transactions, search_query)

    print(matched)
