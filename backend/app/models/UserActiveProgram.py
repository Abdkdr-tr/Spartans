from sqlalchemy import Column, Integer, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.models.base import Base, BaseModelMixin
from datetime import datetime

class UserActiveProgram(Base, BaseModelMixin):
    __tablename__ = 'user_active_program'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    program_id = Column(Integer, ForeignKey("workout_programs.id"))
    assigned_at = Column(DateTime, default=datetime.now, nullable=False)

    user = relationship("User", back_populates="active_programs")
    program = relationship("WorkoutProgram")