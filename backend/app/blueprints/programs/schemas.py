from typing import List, Optional
from pydantic import Field
from app.blueprints.validation import BaseSchema

# ici on défini les schémas qui permettront de faire une validation automatique par Pydantic
# si nous ne devons pas aller beaucoup plus loin dans l'utilsation de Pydantic (pas besoin de faire des decorateurs par exemple),
# c'est parce que APIFlask le fait pour nous. C'est l'approche la plus moderne actuellement

class ExerciseProgramSummary(BaseSchema):
    id: int
    exercise_name: str
    description: Optional[str] = None
    week_number: Optional[int] = None
    set_count: Optional[int] = None
    intensity_rate: Optional[float] = None


class ExerciseProgramCreate(BaseSchema):
    """
    les descriptions s'afficheront dans l'interface de la documentation swaggerUI automatiquement générée par pydantic
    """
    exercise_name: str = Field(..., min_length=2, max_length=120, description="nom de l'exercice", examples=["Développé couché"])
    description: Optional[str] = Field(default=None, description="description de l'exercice")
    week_number: Optional[int] = Field(default=None, description="numéro de la semaine")
    set_count: Optional[int] = Field(default=None, description="nombre de séries")
    intensity_rate: Optional[float] = Field(default=None, description="taux d'intensité")

class ExerciseProgramUpdate(BaseSchema):
    exercise_name: Optional[str] = Field(default=None, min_length=2, max_length=120)
    description: Optional[str] = None
    week_number: Optional[int] = None
    set_count: Optional[int] = None
    intensity_rate: Optional[float] = None


class ExerciseProgramFilter(BaseSchema):
    q: Optional[str] = Field(default=None, description="recherche par pattern textuel dans le nom")
    exercise_name: Optional[str] = Field(default=None, description="filtre par nom d'exercice")
    exerciseprogram_id: Optional[int] = Field(default=None, ge=1, description="filtre par programme d'exercice")
    week_number: Optional[int] = Field(default=None, description="filtre par numéro de semaine")
    set_count: Optional[int] = Field(default=None, description="filtre par nombre de séries")
    intensity_rate: Optional[float] = Field(default=None, description="filtre par taux d'intensité")



class ExerciseProgramResponse(BaseSchema):
    id: int
    exercise_name: str
    description: Optional[str] = None
    week_number: Optional[int] = None
    set_count: Optional[int] = None
    intensity_rate: Optional[float] = None





class ProgramSummary(BaseSchema):
    id: int
    title: str
    description: Optional[str] = None
    target_level: Optional[str] = None
    program_goal: Optional[str] = None
    required_equipment: Optional[str] = None
    exercises: List[ExerciseProgramSummary] = Field(default_factory=list, description="liste des exercices associés au programme")


class ProgramCreate(BaseSchema):
    """
    les descriptions s'afficheront dans l'interface de la documentation swaggerUI automatiquement générée par pydantic
    """
    title: str = Field(..., min_length=2, max_length=120, description="titre du programme", examples=["Programme de musculation"])
    description: Optional[str] = Field(default=None, description="description du programme")
    target_level: Optional[str] = Field(default=None, description="niveau cible", examples=["Débutant", "Intermédiaire", "Avancé"])
    program_goal: Optional[str] = Field(default=None, description="objectif du programme")
    required_equipment: Optional[str] = Field(default=None, description="équipement requis")
    exercises: List[ExerciseProgramCreate] = Field(default_factory=list, description="liste des exercices associés au programme")


class ProgramUpdate(BaseSchema):
    title: Optional[str] = Field(default=None, min_length=2, max_length=120)
    description: Optional[str] = Field(default=None, description="description du programme")
    target_level: Optional[str] = Field(default=None, description="niveau cible", examples=["Débutant", "Intermédiaire", "Avancé"])
    program_goal: Optional[str] = Field(default=None, description="objectif du programme")
    required_equipment: Optional[str] = Field(default=None, description="équipement requis")
    exercises: Optional[List[ExerciseProgramUpdate]] = Field(default=None, description="liste des exercices associés au programme")


class ProgramFilter(BaseSchema):
    q: Optional[str] = Field(default=None, description="recherche par pattern textuel dans le nom")
    exercises: Optional[List[ExerciseProgramFilter]] = Field(default=None, description="filtre par exercices associés")
    target_level: Optional[str] = Field(default=None, description="filtre par niveau cible", examples=["Débutant", "Intermédiaire", "Avancé"])
    program_goal: Optional[str] = Field(default=None, description="filtre par objectif du programme")
    required_equipment: Optional[str] = Field(default=None, description="filtre par équipement requis")


class ProgramResponse(BaseSchema):
    id: int
    title: str
    description: Optional[str] = None
    target_level: Optional[str] = None
    program_goal: Optional[str] = None
    required_equipment: Optional[str] = None
    exercises: List[ExerciseProgramSummary] = Field(default_factory=list, description="liste des exercices associés au programme")