def verify_phone_number(phone_number: str) -> bool:
    """
    Verifies if a phone number is valid
    :param phone_number: str: The phone number to verify
    :return: bool: True if the phone number is valid, False otherwise
    """
    if len(phone_number) != 10:  # check if the phone number is 10 digits long
        return False

    for char in phone_number:  # check if all characters in the phone number are digits
        if not char.isdigit():
            return False

    return True

def verify_email(email: str) -> bool:
    """
    Verifies if an email address is valid
    :param email: str: The email address to verify
    :return: bool: True if the email address is valid, False otherwise
    """
    if "@" not in email or "." not in email:  # check if the email address contains an @ and a .
        return False
    
    if not email.endswith(".com") and not email.endswith(".org"):  
        # check if the email address ends with .com or .org
        return False
    
    return True

def verify_date(date: str) -> bool:
    try:
        year, month, day = date.split("-")
        year, month, day = int(year), int(month), int(day)
    except ValueError:
        return False
    
    if year < 0 or month < 1 or month > 12 or day < 1 or day > 31:
        return False
    
    return True
