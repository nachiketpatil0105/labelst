from sqlalchemy import Column, Integer, Text, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from app.db.session import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"))
    text = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

