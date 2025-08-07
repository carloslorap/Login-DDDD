from abc import ABC, abstractmethod
from app.domain.user import User


class UserRepository(ABC):
    @abstractmethod
    def get_by_email(self, email: str) -> User:
        pass

    @abstractmethod
    def save(self, user: User) -> User:
        pass