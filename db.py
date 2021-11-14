import os
from typing import Iterator

from sqlalchemy import Integer, Column, BOOLEAN, TEXT, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

import config

Base = declarative_base()


class News(Base):
    __tablename__ = 'edupage_news'

    id = Column(Integer, primary_key=True)
    sent = Column(BOOLEAN, default=False)
    title = Column(TEXT)
    description = Column(TEXT)


class Database:
    engine = create_engine(
        "sqlite:///" + os.path.join(os.path.dirname(os.path.realpath(__file__)), config.SQLITE_DATABASE_URL), echo=False)
    SessionMaker = sessionmaker(engine)

    def __init__(self):
        Base.metadata.create_all(bind=self.engine)
        pass

    def create_session(self) -> Iterator[Session]:
        db = self.SessionMaker()
        try:
            yield db
        finally:
            db.close()

    def get_news_by_id(self, id):
        for session in self.create_session():
            return session.query(News).get(id)
