import re
from datetime import datetime, timedelta
import password_handler as ph
import user_handler as uh

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'


def is_old_enough(birthdate):
    today = datetime.today()
    print(today)
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age >= 13


def email_validator(email):
    if not re.fullmatch(regex, email):
        print("Email Regex Fail")
        return False
    else:
        return True


def credential_validation(username, email, password, c_password, dob_year, dob_month, dob_day, gender):
    encrypted_password = ph.encrypt_password(password)

    # Check username length
    if len(username) <= 3 or len(username) >= 15:
        print("Username Length Fail")
        return "Username must be between 3 and 15 characters"

    print("Username Length Pass")

    # Check email format
    if not re.fullmatch(regex, email):
        print("Email Regex Fail")
        return "Invalid Email Address"

    print("Email Regex Pass")

    # Check unique credentials
    if uh.check_unique_cred(username, email) == 0:
        print("Unique Username Fail")
        return "Username already taken, please try again"
    elif uh.check_unique_cred(username, email) == 1:
        print("Unique Email Fail")
        return "Email already taken, please try again"
    elif uh.check_unique_cred(username, email) == 2:
        print("Unique Credentials Pass")

    # check age
    try:
        birthdate = datetime(year=int(dob_year), month=int(dob_month), day=int(dob_day))
        if not is_old_enough(birthdate):
            print("Age Check Fail")
            return "You must be 13 years or older to create an account, Please try again."
    except ValueError:
        print("Invalid Date")
        return "Invalid Date, Please try again."
    print("Valid Age Pass")

    # check gender
    if gender == "Male" or gender == "Female" or gender == "Other":
        pass
    else:
        print("Gender Check Fail")
        return "Invalid Gender, Please try again."

    # Verify password match
    if not ph.verify_password(c_password, encrypted_password):
        print("Password Match Fail")
        return "passwords must match"
    print("Password Match Pass")

    # Check password length
    if len(c_password) < 10:
        print("Password Length Fail")
        return "password must be at least 10 characters"

    print("Password Length Pass")
    print("Validation Passed")
    return None


def journal_validate(title, mood, color, content):
    if len(title) == 0 or len(title) > 25:
        print("Title Length Fail")
        return 1
    if mood != "happy" and mood != "sad" and mood != "angry" and mood != "scared" and mood != "tired":
        print("Mood Check Fail")
        return 2
    if (color != "yellow" and color != "red" and color != "blue" and color != "orange" and color != "green" and color !=
            "greenyellow" and color != "purple" and color != "pink" and color != "white" and color != "black"):
        print("Color Check Fail")
        return 3
    if len(content) == 0 or len(content) > 300:
        print("Content Length Fail")
        return 4
    else:
        print("validate Pass")
        return 5


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
