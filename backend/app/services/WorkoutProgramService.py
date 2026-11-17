from app.models.WorkoutProgramDao import WorkoutProgramDao


class WorkoutProgramService:
    
    def __init__(self):
        self._dao = WorkoutProgramService()
   
    def findAll(self):
        return self._dao.findAll()
     
    def findById(self,user_id: int):
        return self._dao.findById(user_id)
   
   def findAllEmbeddingVectors(self):
       return self._dao.findAllEmbeddingVectors()
   
   def findProgramExercices(self,program_id: int):
       return self._dao.findProgramExercices(program_id)
