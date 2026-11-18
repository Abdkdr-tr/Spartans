from app.models.UserActiveProgramDAO import UserActiveProgramDAO



class UserActiveProgramService:
    
    def __init__(self):
       self._dao = UserActiveProgramDAO()

    def findByUserId(self,user_id: int):
       return self._dao.findByUserId(user_id)
   
    def save_or_update(self,user_id: int,program_data: dict):
       return self._dao.save_or_update(user_id,program_data)

    def delete(self,user_id: int):
      return self._dao.delete(user_id)
