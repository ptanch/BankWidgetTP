from typing import Optional


def get_mask_card_number(card_number: str) -> str:
    """Obtaining card numbers and masking some of them"""

    if len(card_number) < 12:
        raise ValueError("Invalid card number length")

    masked_card_number = card_number.replace(card_number[6:12], "******")

    splits = []

    for i in range(0, len(card_number), 4):
        split = masked_card_number[i:i + 4]  # substring 4 symbols
        splits.append(split)
    splitted_card_number = " ".join(splits)

    return splitted_card_number


def get_mask_account(account_number: str) -> str:
    """Masking number of account"""

    masked_account_number = account_number.replace(account_number[0:-4], "**")

    return masked_account_number


if __name__ == '__main__':

    card_number = str(input("Введите номер карты "))
    print(get_mask_card_number(card_number))  # 7000 79** **** 6361 function output
    account_number = str(input("Введите номер счета "))
    print(get_mask_account(account_number))  # **4305 function output
