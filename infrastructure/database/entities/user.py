from infrastructure.database.entities.base import Base
from sqlalchemy import JSON, String, Column


class User(Base):
    __tablename__ = "Users"
    
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)