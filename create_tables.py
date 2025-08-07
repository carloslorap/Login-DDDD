# create_tables.py
from app.infrastructure.db.connection import Base, engine
from app.infrastructure.models.user_model import UserModel

Base.metadata.create_all(bind=engine)
 