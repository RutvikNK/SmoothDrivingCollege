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
    """
    Verifies if a date is valid
    :param date: str: The date to verify in the format YYYY-MM-DD
    :return: bool: True if the date is valid, False otherwise
    """
    try:
        year, month, day = date.split("-")
        year, month, day = int(year), int(month), int(day)
    except ValueError:
        return False
    
    if year < 0 or month < 1 or month > 12 or day < 1 or day > 31:
        return False
    
    return True

def verify_time(time: str) -> bool:
    """
    Verifies if a time is valid
    :param time: str: The time to verify in the format HH:MM:SS
    :return: bool: True if the time is valid, False otherwise
    """
    try:
        hour, minute, second = time.split(":")
        hour, minute, second = int(hour), int(minute), int(second)
    except ValueError:
        return False
    
    if hour < 0 or hour > 23 or minute < 0 or minute > 59 or second < 0 or second > 59:
        return False
    
    return True

def verify_datetime(datetime: str) -> bool:
    """
    Verifies if a datetime is valid
    :param datetime: str: The datetime to verify in the format YYYY-MM-DD HH:MM:SS
    :return: bool: True if the datetime is valid, False otherwise
    """
    try:
        date, time = datetime.split(" ")
        return verify_date(date) and verify_time(time)
    except ValueError:
        return False

def main():
    date = "2023-10-01"
    time = "12:30:00"
    phone_number = "1234567890"

if __name__ == "__main__":
    main()