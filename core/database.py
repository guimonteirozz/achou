from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from core.config import settings

# Criação do engine utilizando o driver Psycopg 3
engine = create_engine(settings.DATABASE_URL, echo=True, future=True)

# Fábrica de sessões para comunicação com o PostgreSQL
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarativa para os modelos ORM
Base = declarative_base()

def get_db():
    """Dependency para injetar a sessão do banco de dados nas rotas do FastAPI"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()