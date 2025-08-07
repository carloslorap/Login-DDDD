from werkzeug.security import generate_password_hash, check_password_hash

class PasswordHasher:
    def hash(self, password: str) -> str:
        return generate_password_hash(password)

    def verify(self, password: str, hashed: str) -> bool:
        return check_password_hash(hashed, password)