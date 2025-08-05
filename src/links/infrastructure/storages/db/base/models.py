import uuid

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import UUID
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from src.core.db.base import BaseTemplate


class Link(BaseTemplate):
    __tablename__ = "links"

    link_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user = relationship("User", back_populates="links", lazy="selectin")
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False,
    )

    folder = relationship("Folder", back_populates="links", lazy="selectin")
    folder_id = Column(
        UUID(as_uuid=True),
        ForeignKey("folders.folder_id", ondelete="CASCADE"),
        nullable=True,
    )

    name = Column(String, nullable=False)
    original_url = Column(String, nullable=False)
    short_code = Column(String, unique=True, nullable=False)
    clicks = Column(Integer, default=0)

    @hybrid_property
    def is_root(self) -> bool:
        return self.folder_id is None
