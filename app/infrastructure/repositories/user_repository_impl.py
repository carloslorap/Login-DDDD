from app.domain.user import User
from app.domain.user_repository import UserRepository
from app.infrastructure.models.user_model import UserModel
from app.infrastructure.db.connection import SessionLocal
 
class UserRepositoryImpl(UserRepository):
    def get_by_email(self, email: str):
        with SessionLocal() as db:
            user_row = db.query(UserModel).filter(UserModel.email == email).first()
            if user_row:
                return User(
                    id=user_row.id,
                    username=user_row.username,
                    email=user_row.email,
                    password=user_row.password
                )
            return None

    def save(self, user: User):
        with SessionLocal() as db:
            user_model = UserModel(
                username=user.username,
                email=user.email,
                password=user.password
            )
            db.add(user_model)
            db.commit()
            db.refresh(user_model)

            return User(
                id=user_model.id,
                username=user_model.username,
                email=user_model.email,
                password=user_model.password
            )
