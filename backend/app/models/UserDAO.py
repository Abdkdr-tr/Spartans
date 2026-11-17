from typing import Optional, List, Dict, Any
from app.models.User import User
from app.models.UserDAOInterface import UserDAOInterface
from app.models.base import get_session_factory
from flask import current_app

class UserDAO(UserDAOInterface):

    def __init__(self, db_uri: Optional[str] = None):
        if db_uri is None:
            db_uri = current_app.config.get('SQLALCHEMY_DATABASE_URI')
        self.SessionFactory = get_session_factory(db_uri)

    def connect(self):
        return self.SessionFactory()

    def findAll(self) -> List[User]:
        with self.connect() as session:
            return session.query(User).all()

    def findById(self, user_id: int) -> Optional[User]:
        with self.connect() as session:
            return session.query(User).filter(User.id == user_id).first()

    def add(self, user_data: dict) -> User:
        with self.connect() as session:
            new_user = User(**user_data)
            session.add(new_user)
            session.commit()
            created_id = new_user.id
        return self.findById(created_id)

    def delete(self, user_id: int) -> bool:
        with self.connect() as session:
            user = session.query(User).filter(User.id == user_id).first()
            if user:
                session.delete(user)
                session.commit()
                return True
            return False