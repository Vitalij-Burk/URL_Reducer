import uuid

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import UUID
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from src.core.db.base import BaseTemplate


class Folder(BaseTemplate):
    __tablename__ = "folders"

    folder_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user = relationship("User", back_populates="folders")
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False,
    )

    parent = relationship(
        "Folder", remote_side=[folder_id], back_populates="children", lazy="selectin"
    )
    parent_id = Column(
        UUID(as_uuid=True),
        ForeignKey("folders.folder_id", ondelete="CASCADE"),
        nullable=True,
    )

    links = relationship("Link", back_populates="folder", cascade="all, delete-orphan")
    children = relationship(
        "Folder", back_populates="parent", cascade="all, delete-orphan", lazy="selectin"
    )

    name = Column(String, nullable=False)

    @hybrid_property
    def is_root(self) -> bool:
        return self.parent_id is None
