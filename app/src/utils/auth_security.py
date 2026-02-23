from pwdlib import PasswordHash


password_hash = PasswordHash.recommended()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return password_hash.verify(plain_password, hashed_password)
    except ValueError:
        return False


def get_password_hash(password: str):
    return password_hash.hash(password)
