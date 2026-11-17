from typing import Optional, Dict, Any
from app.models.UserActiveProgram import UserActiveProgram
from app.models.UserActiveProgramDAOInterface import UserActiveProgramDAOInterface
from app.models.base import get_session_factory
from sqlalchemy.orm import joinedload
from flask import current_app

class UserActiveProgramDAO(UserActiveProgramDAOInterface):

    def __init__(self, db_uri: Optional[str] = None):
        if db_uri is None:
            db_uri = current_app.config.get('SQLALCHEMY_DATABASE_URI')
        self.SessionFactory = get_session_factory(db_uri)

    def connect(self):
        return self.SessionFactory()

    def findByUserId(self, user_id: int) -> Optional[UserActiveProgram]:
        with self.connect() as session:
            return (
                session.query(UserActiveProgram)
                .options(joinedload(UserActiveProgram.program))
                .filter(UserActiveProgram.user_id == user_id)
                .first()
            )

    def save_or_update(self, user_id: int, program_data: dict) -> UserActiveProgram:
        with self.connect() as session:
            active_program = session.query(UserActiveProgram).filter(UserActiveProgram.user_id == user_id).first()
            
            if active_program:
                for key, value in program_data.items():
                    setattr(active_program, key, value)
            else:
                active_program = UserActiveProgram(user_id=user_id, **program_data)
                session.add(active_program)
                
            session.commit()
            
        return self.findByUserId(user_id)

    def delete(self, user_id: int) -> bool:
        with self.connect() as session:
            active = session.query(UserActiveProgram).filter(UserActiveProgram.user_id == user_id).first()
            if active:
                session.delete(active)
                session.commit()
                return True
            return False