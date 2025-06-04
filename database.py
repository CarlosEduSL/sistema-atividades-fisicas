import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuração flexível de banco
DATABASE_URL = os.getenv("DATABASE_URL")

# Fallback para desenvolvimento local
if not DATABASE_URL:
    DATABASE_URL = "sqlite:///./test.db"
    print("⚠️  Usando SQLite local")

# ✅ SOLUÇÃO: Configuração condicional por tipo de banco
if DATABASE_URL.startswith("sqlite"):
    # SQLite: precisa do check_same_thread=False
    engine = create_engine(
        DATABASE_URL, 
        connect_args={"check_same_thread": False}
    )
    print("🗄️  Configurado para SQLite")
else:
    # PostgreSQL/MySQL: sem connect_args
    engine = create_engine(DATABASE_URL)
    print("🐘 Configurado para PostgreSQL")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
