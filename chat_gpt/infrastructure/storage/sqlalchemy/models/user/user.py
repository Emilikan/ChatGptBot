from sqlalchemy import Column, String, Integer, BigInteger, Boolean
from chat_gpt.infrastructure.storage.sqlalchemy.models import Base
from chat_gpt.core import entities


class User(Base):
    __tablename__ = "user"

    id = Column(BigInteger, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    number_requests = Column(Integer, nullable=False, default=0)
    access = Column(Boolean, nullable=False, default=False)
    is_admin = Column(Boolean, nullable=False, default=False)


def user_mapping():
    table = User.__table__
    Base.registry.map_imperatively(
        entities.User,
        table,
    )
