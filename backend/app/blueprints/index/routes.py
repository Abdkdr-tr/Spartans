from apiflask import APIBlueprint

index_bp = APIBlueprint('index', __name__)

@index_bp.get('/')
def index():
    """Page d'accueil de l'API REST"""
    return {
        "message": "API REST de la SAE 203 - Spartans",
        "docs": "/docs",
        "openapi": "/openapi.json",
        "endpoints": {
            "health": "/api/health",
            "users": "/api/users",
            "programs": "/api/programs/<int:id>",
        }
    }