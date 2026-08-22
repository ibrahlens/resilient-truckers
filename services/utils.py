import re


# =====================================
# Kenyan Phone Number Utilities
# =====================================

def is_valid_phone_number(phone_number):
    """
    Validate a Kenyan phone number.

    Accepted examples:

        0712345678
        0112345678
        712345678
        112345678
        +254712345678
        +254112345678
        254712345678
        254112345678

    Returns:
        True  -> valid Kenyan phone number
        False -> invalid phone number
    """

    if not phone_number:
        return False

    phone = re.sub(
        r"\D",
        "",
        str(phone_number).strip()
    )

    # Convert local format to international format
    if phone.startswith("0"):

        phone = "254" + phone[1:]

    elif phone.startswith("7") or phone.startswith("1"):

        phone = "254" + phone

    # Validate Kenyan mobile number
    return bool(
        re.fullmatch(
            r"254(7|1)\d{8}",
            phone
        )
    )