from typing import Generator

from sqlalchemy import create_engine
from sqlmodel import Session

from core.config import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URL)

DbSession = Session(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    #         """
    # データベースセッションを取得するジェネレータ関数

    # Returns:
    #     DbSession: データベースセッションオブジェクト
    # """
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()