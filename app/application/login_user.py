from app.domain.user_repository import UserRepository
from app.infrastructure.auth.password_hasher import PasswordHasher


class LoginUser:
    def __init__(self, user_repository: UserRepository, password_hasher: PasswordHasher):
        self.user_repository = user_repository
        self.password_hasher = password_hasher

    def execute(self, email: str, password: str):
        user = self.user_repository.get_by_email(email)

        if user is None:
            raise ValueError("Usuario no encontrado.")

        if not self.password_hasher.verify(password, user.password):
            raise ValueError("Contraseña incorrecta.")

        return user
