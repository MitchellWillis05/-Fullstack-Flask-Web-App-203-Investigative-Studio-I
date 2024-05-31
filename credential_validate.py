import re
import password_handler as ph
import user_handler as uh

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'


def credential_validation(username, email, password, c_password):
    encrypted_password = ph.encrypt_password(password)

    # Check username length
    if len(username) < 6:
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
        print("Unique credentials Pass")

    print("Validation Passed")
    if uh.create_new_user(username, email, encrypted_password):
        print("User Created")
        return ""
    else:
        print("User Creation Failed")
        return "An error occurred, please try again"

