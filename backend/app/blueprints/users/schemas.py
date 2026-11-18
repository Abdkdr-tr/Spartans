from typing import Optional
from pydantic import Field
from app.blueprints.validation import BaseSchema

# ici on défini les schémas qui permettront de faire une validation automatique par Pydantic
# si nous ne devons pas aller beaucoup plus loin dans l'utilsation de Pydantic (pas besoin de faire des decorateurs par exemple),
# c'est parce que APIFlask le fait pour nous. C'est l'approche la plus moderne actuellement

class UserSummary(BaseSchema):
    id: int
    name: str


class UserCreate(BaseSchema):
    """
    les descriptions s'afficheront dans l'interface de la documentation swaggerUI automatiquement générée par pydantic
    """
    full_name: str = Field(..., min_length=2, max_length=120, description="nom completde l'utilisateur", examples=["Michael Jordan"])
    fitness_level: Optional[str] = Field(default=None, description="niveau de condition physique de l'utilisateur", examples=["Débutant", "Intermédiaire", "Avancé"])
    primary_goal: Optional[str] = Field(default=None, description="objectif principal", examples=["Perte de poids", "Prise de masse", "Garder une bonne condition physique"])
    medical_constraints: Optional[str] = Field(default=None, description="contraintes médicales de l'utilisateur", examples=["Aucune", "Problèmes cardiaques", "Blessures"])


class UserUpdate(BaseSchema):
    full_name: Optional[str] = Field(default=None, min_length=2, max_length=120)
    fitness_level: Optional[str] = Field(default=None, description="niveau de condition physique de l'utilisateur")
    primary_goal: Optional[str] = Field(default=None, description="objectif principal")
    medical_constraints: Optional[str] = Field(default=None, description="contraintes médicales de l'utilisateur", examples=["Aucune", "Problèmes cardiaques", "Blessures"])


class UserFilter(BaseSchema):
    q: Optional[str] = Field(default=None, description="recherche par pattern textuel dans le nom")
    fitness_level: Optional[str] = Field(default=None, description="filtre par niveau de condition physique")
    primary_goal: Optional[str] = Field(default=None, description="filtre par objectif principal")
    medical_constraints: Optional[str] = Field(default=None, description="filtre par contraintes médicales")


class UserResponse(BaseSchema):
    id: int
    full_name: str
    fitness_level: Optional[str] = None
    primary_goal: Optional[str] = None
    medical_constraints: Optional[str] = None