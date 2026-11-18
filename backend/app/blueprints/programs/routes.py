from typing import List
from apiflask import APIBlueprint, abort
from app.services.WorkoutProgramService import WorkoutProgramService
from app.blueprints.programs.schemas import ProgramFilter, ProgramResponse, ProgramResponse
from app.blueprints.programs.schemas import ExerciseProgramFilter, ExerciseProgramResponse, ExerciseProgramResponse
# tag permet de ranger les endpoints de clothes dans une section accordéon nommée Clothes 
# (uniquement utile pour la génération automatique de la documentation swaggerUI)
program_bp = APIBlueprint('program', __name__, tag='Programs')

# on déclare d'abord la route
@program_bp.get("")
# on prend ce qui vient et on filtre l'input (l'entrée)
# arg_name indique l'argument qu'on va analyser, location indique l'emplacement dans la requête HTTP
@program_bp.input(ProgramFilter, location='query', arg_name='query')
# on indique ce qui doit être retourné : ici une liste de JSON suivant le schéma ProgramResponse 
# (donc ce sera une liste d'instance de ProgramResponse qui seront sérialisées avec jsonify) Nous n'avons pas besoin de jsonify nous-même grâce à APIFlask
@program_bp.output(ProgramResponse)
def list_programs(query: ProgramFilter):
    """liste tous les programmes avec filtrage (Read du CRUD)"""
    wps = WorkoutProgramService()
    # model_dump() donne la version serialisée automatiquement (jsonify). exclude_unset permet d'être plus flexible au niveau des clés/champs non définis
    return wps.findAll(**query.model_dump(exclude_unset=True))


@program_bp.get('/<int:program_id>')
@program_bp.output(ProgramResponse)
def get_program(program_id: int):
    """obtient un programme avec ses détails (Read du CRUD)"""
    wps = WorkoutProgramService()
    program = wps.findById(program_id)
    if not program:
        abort(404, f"Programme {program_id} introuvable")
    return program

"""
@program_bp.post('')
@program_bp.input(ProgramCreate, arg_name='body')
@program_bp.output(ProgramResponse, status_code=201)
def create_program(body: ProgramCreate):
    #crée un nouveau programme (Create du CRUD)
    wps = WorkoutProgramService()
    try:
        return wps.add(body.model_dump())
    except ValueError as e:
        abort(400, str(e))

# plutôt que de faire plusieurs raccourci bp.patch() bp.put() on utilise l'approche standard avec bp.route(methods=[])
@program_bp.route('/<int:program_id>', methods=['PUT', 'PATCH'])
@program_bp.input(ProgramUpdate, arg_name='body')
@program_bp.output(ProgramResponse)
def update_program(program_id: int, body: ProgramUpdate):
    #met à jour un programme (Update du CRUD)
    wps = WorkoutProgramService()
    updated = wps.update(program_id, body.model_dump(exclude_unset=True))
    if not updated:
        abort(404, f"Programme {program_id} introuvable")
    return updated

@program_bp.delete('/<int:program_id>')
@program_bp.output({}, status_code=204)
def delete_program(program_id: int):
    #supprime un programme
    wps = WorkoutProgramService()
    success = wps.delete(program_id)
    if not success:
        abort(404, f"Programme {program_id} introuvable")
    return ''
"""



#On fait la même chose pour les exercices associés aux programmes
@program_bp.get("")
@program_bp.input(ExerciseProgramFilter, location='query', arg_name='query')
@program_bp.output(ExerciseProgramResponse)
def list_exercises(query: ExerciseProgramFilter):
    """liste tous les programmes avec filtrage (Read du CRUD)"""
    wps = WorkoutProgramService()
    # model_dump() donne la version serialisée automatiquement (jsonify). exclude_unset permet d'être plus flexible au niveau des clés/champs non définis
    return wps.findAll(**query.model_dump(exclude_unset=True))


@program_bp.get('/<int:program_id>')
@program_bp.output(ExerciseProgramResponse)
def get_exercise(program_id: int):
    """obtient un exercice avec ses détails (Read du CRUD)"""
    wps = WorkoutProgramService()
    exercise = wps.findById(program_id)
    if not exercise:
        abort(404, f"Exercice {program_id} introuvable")
    return exercise

"""
@program_bp.post('')
@program_bp.input(ExerciseProgramCreate, arg_name='body')
@program_bp.output(ExerciseProgramResponse, status_code=201)
def create_exercise(body: ExerciseProgramCreate):
    #crée un nouvel exercice (Create du CRUD)
    wps = WorkoutProgramService()
    try:
        return wps.add(body.model_dump())
    except ValueError as e:
        abort(400, str(e))

# plutôt que de faire plusieurs raccourci bp.patch() bp.put() on utilise l'approche standard avec bp.route(methods=[])
@program_bp.route('/<int:program_id>', methods=['PUT', 'PATCH'])
@program_bp.input(ExerciseProgramUpdate, arg_name='body')
@program_bp.output(ExerciseProgramResponse)
def update_exercise(program_id: int, body: ExerciseProgramUpdate):
    #met à jour un exercice (Update du CRUD)
    wps = WorkoutProgramService()
    updated = wps.update(program_id, body.model_dump(exclude_unset=True))
    if not updated:
        abort(404, f"Exercice {program_id} introuvable")
    return updated


@program_bp.delete('/<int:program_id>')
@program_bp.output({}, status_code=204)
def delete_exercise(program_id: int):
    #supprime un exercice
    wps = WorkoutProgramService()
    success = wps.delete(program_id)
    if not success:
        abort(404, f"Exercice {program_id} introuvable")
    return ''
"""


@program_bp.get('/<int:program_id>/exercises')
@program_bp.output(List[ExerciseProgramResponse])
def get_exercises_of_program(program_id: int):
    """obtient tous les exercices associés à un programme"""
    wps = WorkoutProgramService()
    exercises = wps.get_exercises_for_program(program_id)
    if exercises is None:
        abort(404, f"Programme {program_id} introuvable")
    return exercises