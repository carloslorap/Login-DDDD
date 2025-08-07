from app.domain.user import User
from app.domain.user_repository import UserRepository
from app.infrastructure.auth.password_hasher import PasswordHasher


class RegisterUser:
    def __init__(self, user_repository: UserRepository, password_hasher: PasswordHasher):
        self.user_repository = user_repository
        self.password_hasher = password_hasher

    def execute(self, username: str, email: str, password: str) -> User:
        if not username or not email or not password:
            raise ValueError("Todos los campos son obligatorios.")

        existing_user = self.user_repository.get_by_email(email)
        if existing_user:
            raise ValueError("El correo ya está registrado.")

        hashed_password = self.password_hasher.hash(password)
        new_user = User(id=None, username=username, email=email, password=hashed_password)

        return self.user_repository.save(new_user)
