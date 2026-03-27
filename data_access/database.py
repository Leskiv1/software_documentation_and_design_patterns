from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data_access.models import Base

# Створюємо файл бази даних steam_app.db у корені проєкту
SQLALCHEMY_DATABASE_URL = "sqlite:///./steam_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Створює всі таблиці в базі даних, якщо їх ще немає."""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Генератор сесій БД для FastAPI (Dependency Injection)."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()