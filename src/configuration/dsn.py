import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import yaml

file_path = os.path.join(os.path.dirname(__file__), 'config.yml')
with open(file_path) as f:
    db_config = yaml.safe_load(f)["dsn"]

SQLALCHEMY_DATABASE_URL = f'postgresql://{db_config["user"]}:{db_config["password"]}@{db_config["host"]}:{db_config["port"]}/{db_config["database"]}'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
