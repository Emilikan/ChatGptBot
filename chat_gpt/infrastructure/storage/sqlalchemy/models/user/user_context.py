from sqlalchemy import Column, Integer, BigInteger, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from chat_gpt.infrastructure.storage.sqlalchemy.models import Base
from chat_gpt.core import entities


class UserContext(Base):
    __tablename__ = "user_context"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        BigInteger,
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    context = Column(JSONB)


def user_context_mapping():
    table = UserContext.__table__
    Base.registry.map_imperatively(
        entities.UserContext,
        table,
    )
