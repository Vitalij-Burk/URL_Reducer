import uuid

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import UUID
from sqlalchemy.orm import relationship

from core.db.models import BaseTemplate


class User(BaseTemplate):
    __tablename__ = "users"

    links = relationship("Link", back_populates="user", lazy="select")
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)


class Link(BaseTemplate):
    __tablename__ = "links"

    user = relationship("User", back_populates="links")
    link_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False,
    )
    name = Column(String, nullable=False)
    entry_link = Column(String, nullable=False)
    short_link = Column(String, unique=True, nullable=False)
    clicks = Column(Integer, default=0)
