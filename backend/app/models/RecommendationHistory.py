from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base, BaseModelMixin


class RecommendationHistory(Base, BaseModelMixin):
    __tablename__ = 'recommendation_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    recommendation_method = Column(String(100))
    user_query = Column(Text)
    raw_output = Column(Text)
    execution_time_ms = Column(Integer)
    user_feedback = Column(Text)

    user = relationship("User", back_populates="recommendations")