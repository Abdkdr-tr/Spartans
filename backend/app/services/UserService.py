from app.models.UserDao import UserDao



class UserService:


   def __init__(self):
      self._dao = UserDao()
   
   def findAll(self):
       return self._dao.findAll()
   
   def findById(self,user_id: int):
       return self.dao.findById(user_id)
  
   def add(self,user_data: dict):
       return self._dao.add(user_data)
   
   def delete(self,user_id: int):
       return self._dao.delete(user_id)
