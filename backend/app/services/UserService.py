from app.models.UserDAO import UserDAO



class UserService:


   def __init__(self):
      self._dao = UserDAO()
   
   def findAll(self):
       return self._dao.findAll()
   
   def findById(self,user_id: int):
       return self._dao.findById(user_id)
  
   def add(self,user_data: dict):
       return self._dao.add(user_data)
   
   def delete(self,user_id: int):
       return self._dao.delete(user_id)

   """
   Pas encore existant dans UserDAO, mais pourrait être utile pour l'avenir.

   def update(self,user_id: int, user_data: dict):
       return self._dao.update(user_id, user_data)

   def get_all(self, **filters):
       return self._dao.get_all(**filters)

   def get_by_id(self, user_id: int):
       return self._dao.get_by_id(user_id)

   def create(self, user_data: dict):
       return self._dao.create(user_data)"""