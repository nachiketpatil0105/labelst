from sqlalchemy import Column, Integer, String, JSON, TIMESTAMP
from sqlalchemy.sql import func
from app.db.session import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    labels = Column(JSON, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
