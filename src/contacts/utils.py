import re


def is_valid_israeli_phone(phone: str) -> bool:
    israeli_phone_regex = r"^(05\d{8}|\+9725\d{8})$"
    return bool(re.match(israeli_phone_regex, phone))
