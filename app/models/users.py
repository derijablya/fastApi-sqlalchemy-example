from sqlalchemy import Column, String
from app.models import Base
from app.services.utils import hashing


class Users(Base):
    username = Column(String(64), index=True, unique=True)
    email = Column(String(120), index=True, unique=True)
    password = Column(String(128))

    def __init__(self, name, email, password):
        self.username = name
        self.email = email
        self.password = hashing.get_password_hash(password)

    def check_password(self, password):
        return hashing.verify_password(password, self.password)
