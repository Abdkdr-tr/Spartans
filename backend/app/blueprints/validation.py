from pydantic import BaseModel, ConfigDict

class BaseSchema(BaseModel):
    """
    schéma pydantic. sera hérité par les autres. permet de ne pas avoir à recréer la confid pydantic à chaque fois
    """
    model_config = ConfigDict(
        # pour permettre de sérialiser directement les instances orm
        from_attributes=True,
        # permet de charger les données sans dépendre du nom exact du champ python/schéma
        populate_by_name=True,
        # applique .strip() automatiquement
        str_strip_whitespace=True
    )