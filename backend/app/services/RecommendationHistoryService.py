from app.models.RecommendationHistoryDAO import RecommendationHistoryDAO




class RecommendationHistoryService:
    
   def __init__(self):
     self._dao = RecommendationHistoryDAO()

   def findAll(self):
      return self._dao.findAll()
   
   def findById(self,history_id: int): 
      return self._dao.findById(history_id)
  
   def findByUserId(self,user_id: int):
      return self._dao.findByUserId(user_id)
  
   def add(self,history_data: dict):
      return self._dao.add(history_data)
  
   def delete(self,history_id: int):
      return self._dao.delete(history_id)
