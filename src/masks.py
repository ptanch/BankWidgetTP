import logging
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_PATH = os.path.join(BASE_DIR, 'logs', 'info.log')

os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)


logger = logging.getLogger('masks')
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(LOG_PATH, mode='w', encoding='utf-8')
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_mask_card_number(card_number: str) -> str:
    """Obtaining card numbers and masking some of them"""

    logger.debug("Start masking card number")

    try:
        if not isinstance(card_number, str):
            raise TypeError("Card number must be a string.")
        if len(card_number) < 12:
            raise ValueError("Card number is too short to be masked.")
        if not card_number.isdigit():
            raise ValueError("Card number must contain only digits.")
    except Exception as e:
        logger.error(f"Error in get_mask_card_number: {e}")
        raise

    masked_card_number = card_number[:6] + "******" + card_number[12:]

    splits = []

    for i in range(0, len(card_number), 4):
        split = masked_card_number[i:i + 4]  # substring 4 symbols
        splits.append(split)
    splitted_card_number = " ".join(splits)

    logger.info(f"Successfully masked card number: {splitted_card_number}")
    return splitted_card_number


def get_mask_account(account_number: str) -> str:
    """Masking number of account"""

    logger.debug("Start masking account number")

    try:
        if not isinstance(account_number, str):
            raise TypeError("Account number must be a string.")
        if len(account_number) < 4:
            raise ValueError("Account number is too short to mask.")

    except Exception as e:
        logger.error(f"Error in get_mask_account: {e}")
        raise

    result = "**" + account_number[-4:]
    logger.info(f"Successfully masked account number: {result}")
    return result


if __name__ == '__main__':  # pragma: no cover
    try:
        card_number = str(input("Введите номер карты "))
        print(get_mask_card_number(card_number))  # 7000 79** **** 6361 function output

        account_number = str(input("Введите номер счета "))
        print(get_mask_account(account_number))  # **4305 function output
    except Exception as e:
        logger.critical(f"Unhandled exception in main: {e}")
