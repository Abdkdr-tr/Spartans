from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base, BaseModelMixin


class ProgramExercise(Base, BaseModelMixin):
    __tablename__ = 'program_exercises'

    id = Column(Integer, primary_key=True, autoincrement=True)
    program_id = Column(Integer, ForeignKey("workout_programs.id"))
    exercise_name = Column(String(255), nullable=False)
    week_number = Column(Integer)
    day_number = Column(Integer)
    set_count = Column(Integer)
    rep_count = Column(String(50))
    intensity_rate = Column(Float)

    program = relationship("WorkoutProgram", back_populates="exercises")