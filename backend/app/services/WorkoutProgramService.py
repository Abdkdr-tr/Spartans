from app.models.WorkoutProgramDAO import WorkoutProgramDAO


class WorkoutProgramService:
    
    def __init__(self):
        self._dao = WorkoutProgramDAO()
   
    def findAll(self):
        return self._dao.findAll()
     
    def findById(self,user_id: int):
        return self._dao.findById(user_id)
   
    def findAllEmbeddingVectors(self):
       return self._dao.findAllEmbeddingVectors()
    
    """
    Pas encore existant dans WorkoutProgramDAO, mais pourrait être utile pour l'avenir.

    def findProgramExercices(self,program_id: int):
       return self._dao.findProgramExercices(program_id)

    def add(self, program_data: dict):
        return self._dao.add(program_data)

    def update(self, program_id: int, program_data: dict):
        return self._dao.update(program_id, program_data)

    def delete(self, program_id: int):
        return self._dao.delete(program_id)
    """

    def get_exercises_for_program(self, program_id: int):
        return self._dao.get_exercises_for_program(program_id)