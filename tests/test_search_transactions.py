import pytest
from src.search_transactions import process_bank_search


SAMPLE_DATA = [
    {'id': 1, 'amount': 100, 'description': 'Оплата мобильной связи'},
    {'id': 2, 'amount': 250, 'description': 'Покупка в супермаркете'},
    {'id': 3, 'amount': 500, 'description': 'Перевод другу'},
    {'id': 4, 'amount': 120, 'description': 'Связь и интернет'},
    {'id': 5, 'amount': 50}  # элемент без поля description — не должен ломать поиск
]


def test_basic_match():
    """Находим одну операцию с точным совпадением подстроки."""
    result = process_bank_search(SAMPLE_DATA, 'связи')
    assert result == [
        {'id': 1, 'amount': 100, 'description': 'Оплата мобильной связи'}
    ]


def test_case_insensitive_and_multiple_matches():
    """
    Поиск нечувствителен к регистру и находит
    все операции, где встречается подстрока.
    """
    result = process_bank_search(SAMPLE_DATA, 'СвЯЗ')
    ids = {op['id'] for op in result}
    assert ids == {1, 4}
    assert len(result) == 2


def test_no_match_returns_empty_list():
    """Если совпадений нет, возвращается пустой список."""
    result = process_bank_search(SAMPLE_DATA, 'кафе')
    assert result == []
