import re
from datetime import datetime, timedelta
import password_handler as ph
import user_handler as uh

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'


def is_old_enough(birthdate):
    today = datetime.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age >= 13


def credential_validation(username, email, password, c_password, dob_year, dob_month, dob_day):
    encrypted_password = ph.encrypt_password(password)

    # Check username length
    if len(username) <= 3 | len(username) >= 15:
        print("Username Length Fail")
        return "An error occurred, please try again"

    print("Username Length Pass")

    # Check email format
    if not re.fullmatch(regex, email):
        print("Email Regex Fail")
        return "An error occurred, please try again"

    print("Email Regex Pass")

    # Check password length
    if len(c_password) < 10:
        print("Password Length Fail")
        return "An error occurred, please try again"

    print("Password Length Pass")

    # Verify password match
    if not ph.verify_password(c_password, encrypted_password):
        print("Password Match Fail")
        return "An error occurred, please try again"

    print("Password Match Pass")

    # Check unique credentials
    if uh.check_unique_cred(username, email) == 0:
        print("Unique Username Fail")
        return "Username already taken, please try again"
    elif uh.check_unique_cred(username, email) == 1:
        print("Unique Email Fail")
        return "Email already taken, please try again"
    elif uh.check_unique_cred(username, email) == 2:
        print("Unique Credentials Pass")

    try:
        birthdate = datetime(year=int(dob_year), month=int(dob_month), day=int(dob_day))
        if not is_old_enough(birthdate):
            print("Age Check Fail")
            return "You must be 13 years or older to create an account, Please try again."
    except ValueError:
        print("char check fail")
        return "Invalid Age, Please try again."
    print("Valid Age Pass")

    print("Validation Passed")
    if uh.create_new_user(username, email,
                          encrypted_password,
                          dob_day, dob_year, dob_year,
                          get_star_sign(int(dob_day), int(dob_month))):
        print("User Created")
        return ""
    else:
        print("User Creation Failed")
        return "An error occurred, please try again"


def get_star_sign(day, month):
    if (month == 1 and day >= 20) or (month == 2 and day <= 18):
        return "Aquarius"
    elif (month == 2 and day >= 19) or (month == 3 and day <= 20):
        return "Pisces"
    elif (month == 3 and day >= 21) or (month == 4 and day <= 19):
        return "Aries"
    elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
        return "Taurus"
    elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
        return "Gemini"
    elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
        return "Cancer"
    elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
        return "Leo"
    elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
        return "Virgo"
    elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
        return "Libra"
    elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
        return "Scorpio"
    elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
        return "Sagittarius"
    elif (month == 12 and day >= 22) or (month == 1 and day <= 19):
        return "Capricorn"
    else:
        return "Invalid date"
