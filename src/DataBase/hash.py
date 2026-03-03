from passlib.context import CryptContext

password_security=CryptContext(schemes='bcrypt',deprecated="auto")

class Hash:
    def encode(password:str):
        return password_security.encrypt(password)

    def verify(password: str, encrypted_password: str):
        return password_security.verify(password, encrypted_password)

