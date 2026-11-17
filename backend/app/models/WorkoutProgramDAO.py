from typing import Optional, List, Tuple
from app.models.ProgramExercise import ProgramExercise
from app.models.WorkoutProgram import WorkoutProgram
from app.models.WorkoutProgramDAOInterface import WorkoutProgramDAOInterface
from app.models.base import get_session_factory
from sqlalchemy.orm import selectinload
from flask import current_app

class WorkoutProgramDAO(WorkoutProgramDAOInterface):

    def __init__(self, db_uri: Optional[str] = None):
        if db_uri is None:
            db_uri = current_app.config.get('SQLALCHEMY_DATABASE_URI')
        self.SessionFactory = get_session_factory(db_uri)

    def connect(self):
        return self.SessionFactory()

    def findAll(self) -> List[WorkoutProgram]:
        with self.connect() as session:
            return session.query(WorkoutProgram).options(selectinload(WorkoutProgram.exercises)).order_by(WorkoutProgram.title).all()

    def findById(self, program_id : int)-> Optional[WorkoutProgram]:
        with self.connect() as session:
            return session.query(WorkoutProgram).options(selectinload(WorkoutProgram.exercises)).filter(WorkoutProgram.id == program_id).first()

    def findAllEmbeddingVectors(self) -> list[Tuple[int, bytes]]:
        session = self.connect()

        try:
            rows = session.query(WorkoutProgram.id,WorkoutProgram.embedding_vector).all()

            resultats = []

            for row in rows:
                program_id = row.id 
                embedding_vector = row.embedding_vector

                resultats.append((program_id, embedding_vector))

            return resultats
        finally:
            session.close()

    def findProgramExercises(self, program_id: int) -> List[ProgramExercise]:
        with self.connect() as session:
            return session.query(ProgramExercise).filter(ProgramExercise.program_id == program_id).all()
        

