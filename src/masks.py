def get_mask_card_number(card_number: str) -> str:
    """Obtaining card numbers and masking some of them"""

    if not isinstance(card_number, str):
        raise TypeError("Card number must be a string.")
    if len(card_number) < 12:
        raise ValueError("Card number is too short to be masked.")
    if not card_number.isdigit():
        raise ValueError("Card number must contain only digits.")

    masked_card_number = card_number[:6] + "******" + card_number[12:]

    splits = []

    for i in range(0, len(card_number), 4):
        split = masked_card_number[i:i + 4]  # substring 4 symbols
        splits.append(split)
    splitted_card_number = " ".join(splits)

    return splitted_card_number


def get_mask_account(account_number: str) -> str:
    """Masking number of account"""

    if not isinstance(account_number, str):
        raise TypeError("Account number must be a string.")
    if len(account_number) < 4:
        raise ValueError("Account number is too short to mask.")

    return "**" + account_number[-4:]


if __name__ == '__main__':  # pragma: no cover

    card_number = str(input("Введите номер карты "))
    print(get_mask_card_number(card_number))  # 7000 79** **** 6361 function output
    account_number = str(input("Введите номер счета "))
    print(get_mask_account(account_number))  # **4305 function output
