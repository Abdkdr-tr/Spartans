from sqlalchemy import Column, Integer, String, Text, LargeBinary
from sqlalchemy.orm import relationship
from app.models.base import Base, BaseModelMixin


class WorkoutProgram(Base, BaseModelMixin):
    __tablename__ = 'workout_programs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    target_level = Column(String(255))
    program_goal = Column(String(255))
    required_equipment = Column(String(255))
    embedding_vector = Column(LargeBinary)

    exercises = relationship("ProgramExercise", back_populates="program")