# Carrega .env, monta DATABASE_URL e cria engine + SessionLocal.
# TODO:implementar get_session() (yield) e Base (declarative_base).

# Passos:
# 1) ler env (dotenv) e montar URL postgresql+psycopg2://...
# 2) engine = create_engine(url, pool_pre_ping=True)
# 3) SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
# 4) Base = declarative_base()
# 5) def get_session(): yield session; finally close

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB")

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()