from typing import Optional
from app.domain.auth import Auth
from app.domain.auth_repository import AuthRepository
from app.infrastructure.models.user_model import Usuario  # Modelo de SQLAlchemy adaptado a tbl_usuario
from app.infrastructure.db.connection import SessionLocal

class AuthRepositoryImpl(AuthRepository):
    def get_by_username(self, username: str) -> Optional[Auth]:
        with SessionLocal() as db:
            user_row = db.query(Usuario).filter(Usuario.usuario == username).first()
            if user_row:
                return Auth(
                    usuario_id=user_row.usuario_id,
                    usuario=user_row.usuario,
                    contrasena=user_row.contrasena,
                )
            return None
 
  
