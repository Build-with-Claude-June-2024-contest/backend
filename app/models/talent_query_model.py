import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.orm import relationship

from app.config.database import DBBase


class TalentQuery(DBBase):
    __tablename__ = "talent_queries"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    nature_language_query = Column(Text, nullable=False)
    structured_query = Column(JSONB, nullable=True)
    query_result = Column(ARRAY(JSONB), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(String(36), ForeignKey('users.id'), nullable=True)
    user = relationship("User", back_populates="talent_queries")
