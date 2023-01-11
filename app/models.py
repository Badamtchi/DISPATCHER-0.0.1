from sqlalchemy import Column, Integer, UUID, String, Boolean
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base

class Messages(Base):
    __tablename__ = "messages"

    id = Column(UUID, primary_key=True, nullable=False)
    sender = Column(String, nullable=False)
    receiver = Column(String, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    seen = Column(Boolean, server_default="FALSE", nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class Users(Base):
    __tablename__ = "users"

    phone = Column(String, primary_key=True, nullable=False, unique=True)
    name = Column(String, nullable=True)
    password = Column(String, nullable=False)
    registered_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
