import hashlib


def encrypt_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password, pwhash):
    if hashlib.sha256(password.encode()).hexdigest() == pwhash:
        return True
    return False

