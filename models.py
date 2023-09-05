import os
from atexit import register

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

PG_USER = os.getenv("PG_USER", "app")
PG_PASSWORD = os.getenv("PG_PASSWORD", "123")
PG_DB = os.getenv("PG_DB", "app")
PG_HOST = os.getenv("PG_HOST", "127.0.0.1")
PG_PORT = os.getenv("PG_PORT", "5431")

PG_DSN = f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"

engine = create_engine(PG_DSN)

register(engine.dispose)

Session = sessionmaker(bind=engine)
Base = declarative_base(bind=engine)


class ADS(Base):
    __tablename__ = "advertisements"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False, unique=True, index=True)
    text = Column(String)
    published_at = Column(DateTime, server_default=func.now())
    user = Column(String, nullable=False, unique=True)


Base.metadata.create_all()
