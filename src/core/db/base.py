from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import func
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class BaseTemplate(Base):
    __abstract__ = True
    __table_args__ = {"extend_existing": True}

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
