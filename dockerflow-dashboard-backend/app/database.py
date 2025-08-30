import os
from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker
from .models.base import Base  # tylko Base, żadnych modeli

DATABASE_URL = f"postgresql://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}@{os.environ['DB_HOST']}:{os.environ['DB_PORT']}/{os.environ['DB_NAME']}"

engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def init_db():
    # Import modeli dopiero tutaj, żeby uniknąć circular import
    from .models.user import User
    from .models.project import Project
    from .models.image_details import ImageDetails
    from .models.image_deploy import ImageDeploy

    inspector = inspect(engine)
    # Pobieramy listę tabel w schemacie public
    existing_tables = inspector.get_table_names()

    # Tworzymy tylko te, których jeszcze nie ma
    tables_to_create = [t for t in Base.metadata.sorted_tables if t.name not in existing_tables]

    if tables_to_create:
        Base.metadata.create_all(bind=engine, tables=tables_to_create)