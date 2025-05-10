import re
from re import Match

from masks import get_mask_account, get_mask_card_number


def mask_account(match: Match[str]) -> str:
    """Masking 20-digit card numbers"""

    digits = match.group(1)
    masked_account = get_mask_account(digits)
    return f"Счет {masked_account}"


def mask_card(match: Match[str]) -> str:
    """Masking 16-digit card numbers"""

    digits = match.group()
    return get_mask_card_number(digits)


def mask_account_card(bank_data: str) -> str:
    """Finding card and account numbers
     in a string and masking them"""

    # Checking account numbers
    bank_data = re.sub(r"Счет\s+(\d{20})", mask_account, bank_data)

    # Checking card numbers
    bank_data = re.sub(r'\d{16}', mask_card, bank_data)

    return bank_data


if __name__ == '__main__':
    print(mask_account_card("Счет 73654108430135874305"))
    print(mask_account_card("Visa Platinum 7000792289606361"))
    print(mask_account_card("Maestro 7000792289606361"))


def get_date(full_date: str) -> str:
    """Output of a simplified date"""
    return f"{full_date[8:10]}.{full_date[5:7]}.{full_date[0:4]}"


if __name__ == '__main__':
    print(get_date("2024-03-11T02:26:18.671407"))
