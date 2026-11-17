from typing import Optional, List, Dict, Any
from app.models.RecommendationHistory import RecommendationHistory

class RecommendationHistoryDAOInterface:

    def findById(self, history_id: int) -> Optional[RecommendationHistory]:
        """Retourne l'historique correspondant, ou None s'il n'existe pas."""
        pass

    def findAll(self) -> List[RecommendationHistory]:
        """Retourne tout l'historique des recommandations."""
        pass

    def findByUserId(self, user_id: int) -> List[RecommendationHistory]:
        """Retourne l'historique des recommandations pour un utilisateur donné."""
        pass

    def add(self, history_data: dict) -> RecommendationHistory:
        """Ajoute une entrée d'historique à partir d'un dictionnaire de données."""
        pass

    def delete(self, history_id: int) -> bool:
        """Supprime une entrée de l'historique par son ID."""
        pass