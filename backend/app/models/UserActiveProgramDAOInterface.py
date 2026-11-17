from typing import Optional, Dict, Any
from app.models.UserActiveProgram import UserActiveProgram

class UserActiveProgramDAOInterface:

    def findByUserId(self, user_id: int) -> Optional[UserActiveProgram]:
        """Retourne le programme actif de l'utilisateur, ou None s'il n'en a pas."""
        pass

    def save_or_update(self, user_id: int, program_data: Dict[str, Any]) -> UserActiveProgram:
        """Crée ou met à jour le programme actif d'un utilisateur à partir d'un dictionnaire."""
        pass

    def delete(self, user_id: int) -> bool:
        """Supprime le programme actif d'un utilisateur par son ID utilisateur."""
        pass