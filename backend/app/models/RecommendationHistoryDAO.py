from typing import Optional, List, Dict, Any
from app.models.RecommendationHistory import RecommendationHistory
from app.models.RecommendationHistoryDAOInterface import RecommendationHistoryDAOInterface
from app.models.base import get_session_factory
from sqlalchemy.orm import joinedload
from flask import current_app

class RecommendationHistoryDAO(RecommendationHistoryDAOInterface):

    def __init__(self, db_uri: Optional[str] = None):
            if db_uri is None:
                db_uri = current_app.config.get('SQLALCHEMY_DATABASE_URI')
            self.SessionFactory = get_session_factory(db_uri)
    
    def connect(self):
        return self.SessionFactory()

    def findAll(self) -> List[RecommendationHistory]:
        with self.connect() as session:
            return session.query(RecommendationHistory).options(joinedload(RecommendationHistory.user)).all()

    def findById(self, history_id: int) -> Optional[RecommendationHistory]:
        with self.connect() as session:
            return session.query(RecommendationHistory).options(joinedload(RecommendationHistory.user)).filter(RecommendationHistory.id == history_id).first()

    def findByUserId(self, user_id: int) -> List[RecommendationHistory]:
        with self.connect() as session:
            return session.query(RecommendationHistory).options(joinedload(RecommendationHistory.user)).filter(RecommendationHistory.user_id == user_id).all()

    def add(self, history_data: dict) -> RecommendationHistory:
        with self.connect() as session:
            new_recommendation = RecommendationHistory(**history_data)
            session.add(new_recommendation)
            session.commit()
            created_id = new_recommendation.id
        return self.findById(created_id)

    def delete(self, history_id: int) -> bool:
        with self.connect() as session:
            recommendation = session.query(RecommendationHistory).filter(RecommendationHistory.id == history_id).first()
            if recommendation:
                session.delete(recommendation)
                session.commit()
                return True
            return False
             
    