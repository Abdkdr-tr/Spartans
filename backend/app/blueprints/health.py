from flask import Blueprint, jsonify

health_bp = Blueprint("health", __name__)


@health_bp.get("/health")
def health():
    """Vérifie que l'API répond correctement. Utile pour les tests de disponibilité et de monitoring."""
    return jsonify({"status": "ok"})