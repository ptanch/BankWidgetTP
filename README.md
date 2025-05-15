# Виджет банковских операций для клиента

## Целью проекта является предоставление набора утилитных функций для работы с пользовательскими данными: фильтрации и сортировки по состоянию и дате, а также безопасной маскировки номеров банковских карт и счетов.

### Установка
1. Убедитесь, что у вас установлен Python 3.7 или выше.
2. Клонируйте репозиторий или скопируйте файлы проекта к себе.
3. Установите зависимости (если используете `virtualenv`, активируйте его сначала):
`pip install`

### Использование функций

* `filter_by_state(users_info: list, state: str = 'EXECUTED') -> list`
Фильтрует список операций по заданному состоянию (`state`).

**Пример**

```
from module import filter_by_state

filtered = filter_by_state(info_from_users, state='CANCELED')
print(filtered)
```

* `sort_by_date(users_info: list, state: str = 'EXECUTED', descending: bool = True) -> list`
Фильтрует список по состоянию и сортирует по дате ('date') в порядке убывания (по умолчанию) или возрастания.

**Пример**
```
from module import sort_by_date

sorted_users = sort_by_date(info_from_users)  # по убыванию
sorted_users_asc = sort_by_date(info_from_users, descending=False)  # по возрастанию

print(sorted_users)
```

* `get_mask_card_number(card_number: str) -> str`
Маскирует номер банковской карты, оставляя первые 6 и последние 4 цифры.

**Пример**
```
get_mask_card_number("1234567812345678")
# → '1234 56** **** 5678'
```

* `get_mask_account(account_number: str) -> str`
Маскирует номер банковского счета, оставляя только последние 4 цифры.

**Пример**
```
get_mask_account("40817810099910004312")
# → '**4312'
```

* `mask_card(match: Match[str]) -> str`
Используется для замены 16-значных номеров карт.

**Пример**
```
re.sub(r'\b\d{16}\b', mask_card, text)
```

* `mask_account(match: Match[str]) -> str`
Используется для замены 20-значных номеров счетов.

**Пример**
```
re.sub(r'\b\d{20}\b', mask_account, text)
```

* `mask_account_card(bank_data: str) -> str`
Находит номера карт (16 цифр) и счетов (20 цифр) в произвольной строке и маскирует их.

**Пример**
```
text = "Transfer from card 1234567812345678 to account 40817810099910004312"
masked = mask_account_card(text)

# → "Transfer from card 1234 56** **** 5678 to account **4312"
```
