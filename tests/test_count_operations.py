from src.count_operations import process_bank_operations


def test_exact_matches():
    data = [
        {'description': 'Оплата связи'},
        {'description': 'Связь'},
        {'description': 'Магазин супермаркет'},
        {'description': 'Купил продукты'}
    ]
    categories = ['связь', 'супермаркет', 'продукты']
    result = process_bank_operations(data, categories)
    print(result)
    assert result == {'связь': 1, 'супермаркет': 1, 'продукты': 1}


def test_no_matches():
    data = [
        {'description': 'Перевод другу'},
        {'description': 'Аренда квартиры'},
    ]
    categories = ['связь', 'продукты']
    result = process_bank_operations(data, categories)
    assert result == {}


def test_multiple_matches_in_one_description():
    data = [
        {'description': 'Мобильная связь и покупка продуктов'},
    ]
    categories = ['продукты', 'связь']
    result = process_bank_operations(data, categories)
    # 'продукты' встречается раньше в списке категорий, но в описании 'связь' идёт первой — она будет выбрана
    assert result == {'связь': 1}
