from sqlmodel import Session
from models.user import User


def learn_lesson(db: Session, user: User, lesson_id: int):
    pass
