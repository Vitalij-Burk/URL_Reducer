import uuid

from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import UUID
from sqlalchemy.orm import relationship

from src.core.db.base import BaseTemplate


class User(BaseTemplate):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    folders = relationship(
        "Folder",
        back_populates="user",
        lazy="selectin",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    links = relationship(
        "Link",
        back_populates="user",
        lazy="selectin",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
