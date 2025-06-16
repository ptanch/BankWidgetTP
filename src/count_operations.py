import re
from collections import Counter
from typing import Dict, List


def process_bank_operations(data: List[Dict], categories: List[str]) -> Dict[str, int]:
    # Преобразуем список категорий в список регулярных выражений (игнорируем регистр)
    category_patterns = {cat: re.compile(re.escape(cat), re.IGNORECASE) for cat in categories}

    # Счётчик для количества операций по категориям
    counter = Counter()

    for item in data:
        description = item.get('description', '')
        for category, pattern in category_patterns.items():
            if pattern.search(description):
                counter[category] += 1
                break  # Если одна категория найдена, остальные можно не проверять

    return dict(counter)


if __name__ == "__main__":  # pragma: no cover
    transactions = [
        {'id': 1, 'amount': 100, 'description': 'Оплата мобильной связи'},
        {'id': 2, 'amount': 250, 'description': 'Покупка в супермаркете'},
        {'id': 3, 'amount': 500, 'description': 'Перевод другу'},
        {'id': 4, 'amount': 120, 'description': 'Мобильная связь и интернет'},
        {'id': 5, 'amount': 700, 'description': 'Покупка продуктов'},
    ]

    categories = ['связь', 'супермаркет', 'продукты']

    result = process_bank_operations(transactions, categories)

    print(result)
