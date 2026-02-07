from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from app.db.session import Base

class Annotation(Base):
    __tablename__ = "annotations"

    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey("items.id", ondelete="CASCADE"), unique=True)
    label = Column(String(100), nullable=False)
    updated_at = Column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now()
    )
