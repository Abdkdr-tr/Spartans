from typing import Optional, List, Tuple
from app.models.ProgramExercise import ProgramExercise
from app.models.WorkoutProgram import WorkoutProgram

class WorkoutProgramDAOInterface:

    def findById(self, program_id : int)-> Optional[WorkoutProgram]:
        """Retourne le programme correspondant, ou None s'il n'existe pas."""
        pass

    def findAll(self) -> List[WorkoutProgram]:
        "Retourne tous les programmes disponible en base de données."
        pass

    def findAllEmbeddingVectors(self) -> list[Tuple[int, bytes]]:
        """Retourne (id, vecteur) pour tous les programmes ayant un embedding.

        Le vecteur est en octets bruts (float32), à décoder."""
        pass

    def findProgramExercises(self, program_id: int) -> List[ProgramExercise]:
        """Retourne les exercices d'un programme."""
        pass