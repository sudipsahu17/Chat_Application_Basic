import re

def validate_email(email_id):
    regex = "^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$"
    if re.match(regex, email_id):
        return True
    else:
        return False

def validate_name(string):
    regex = "^[A-Za-z]{3,}$"
    if re.match(regex, string):
        return True
    else:
        return False

def validate_password(password):
    if len(password) < 7:
        return False
    else:
        return True
