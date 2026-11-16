from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.models.base import Base, BaseModelMixin


class User(Base, BaseModelMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(255), nullable=False)
    fitness_level = Column(String(255))
    primary_goal = Column(String(255))
    medical_constraints = Column(Text)

    active_programs = relationship("UserActiveProgram", back_populates="user")
    recommendations = relationship("RecommendationHistory", back_populates="user")