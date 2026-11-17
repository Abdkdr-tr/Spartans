from typing import Optional, List, Dict, Any
from app.models.User import User

class UserDAOInterface:

    def findById(self, user_id: int) -> Optional[User]:
        """Retourne l'utilisateur correspondant, ou None s'il n'existe pas."""
        pass

    def findAll(self) -> List[User]:
        """Retourne tous les utilisateurs disponibles en base de données."""
        pass

    def add(self, user_data: dict) -> User:
        """Ajoute un nouvel utilisateur à partir d'un dictionnaire de données."""
        pass

    def delete(self, user_id: int) -> bool:
        """Supprime un utilisateur par son ID."""
        pass