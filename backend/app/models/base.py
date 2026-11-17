from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from datetime import datetime

Base = declarative_base()


class BaseModelMixin:
    """Ajoute des méthodes utiles aux modèles SQLAlchemy."""

    def __getitem__(self, item):
        """Accède à un attribut comme dans un dictionnaire."""
        if hasattr(self, item):
            return getattr(self, item)
        raise KeyError(f"L'objet '{self.__class__.__name__}' n'a pas l'attribut '{item}'")

    def to_dict(self):
        """Convertit l'objet en dictionnaire.
        """
        result = {}
        for col in self.__table__.columns:
            val = getattr(self, col.name)
            if isinstance(val, datetime):
                val = val.isoformat()
            result[col.name] = val
        return result


def get_engine(db_uri=None):
    """Crée le moteur de connexion à la base.
    """
    if db_uri is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_path = os.path.join(base_dir, 'database', 'spartans.db')
        db_uri = f"sqlite:///{db_path}"
    return create_engine(db_uri, echo=False)


def get_session_factory(db_uri=None):
    """Retourne une fabrique de sessions liée au moteur.
    """
    engine = get_engine(db_uri)
    return sessionmaker(bind=engine, expire_on_commit=False)