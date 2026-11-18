from typing import List
from apiflask import APIBlueprint, abort
from app.services.UserService import UserService
from app.blueprints.users.schemas import UserFilter, UserCreate, UserResponse, UserUpdate
# tag permet de ranger les endpoints de clothes dans une section accordéon nommée Clothes 
# (uniquement utile pour la génération automatique de la documentation swaggerUI)
user_bp = APIBlueprint('user', __name__, tag='Users')

# on déclare d'abord la route
@user_bp.get("")
# on prend ce qui vient et on filtre l'input (l'entrée)
# arg_name indique l'argument qu'on va analyser, location indique l'emplacement dans la requête HTTP
@user_bp.input(UserFilter, location="query", arg_name="query")
# on indique ce qui doit être retourné : ici une liste de JSON suivant le schéma UserResponse 
# (donc ce sera une liste d'instance de UserResponse qui seront sérialisées avec jsonify) Nous n'avons pas besoin de jsonify nous-même grâce à APIFlask
@user_bp.output(List[UserResponse])
def list_users(query: UserFilter):
    """liste tous les utilisateurs avec filtrage (Read du CRUD)"""
    us = UserService()
    # model_dump() donne la version serialisée automatiquement (jsonify). exclude_unset permet d'être plus flexible au niveau des clés/champs non définis
    return us.get_all(**query.model_dump(exclude_unset=True))


@user_bp.get("/<int:user_id>")
@user_bp.output(UserResponse)
def get_user(user_id: int):
    """obtient un utilisateur avec ses détails (Read du CRUD)"""
    us = UserService()
    user = us.get_by_id(user_id)
    if not user:
        abort(404, f"Utilisateur {user_id} introuvable")
    return user


@user_bp.post("")
@user_bp.input(UserCreate, arg_name="body")
@user_bp.output(UserResponse, status_code=201)
def create_user(body: UserCreate):
    """crée un nouveau utilisateur (Create du CRUD)"""
    us = UserService()
    try:
        return us.create(body.model_dump())
    except ValueError as e:
        abort(400, str(e))

# plutôt que de faire plusieurs raccourci bp.patch() bp.put() on utilise l'approche standard avec bp.route(methods=[])
@user_bp.route("/<int:user_id>", methods=["PUT", "PATCH"])
@user_bp.input(UserUpdate, arg_name="body")
@user_bp.output(UserResponse)
def update_user(user_id: int, body: UserUpdate):
    """met à jour un utilisateur (Update du CRUD)"""
    us = UserService()
    updated = us.update(user_id, body.model_dump(exclude_unset=True))
    if not updated:
        abort(404, f"Utilisateur {user_id} introuvable")
    return updated


@user_bp.delete("/<int:user_id>")
@user_bp.output({}, status_code=204)
def delete_user(user_id: int):
    """supprime un utilisateur"""
    us = UserService()
    success = us.delete(user_id)
    if not success:
        abort(404, f"Utilisateur {user_id} introuvable")
    return ''