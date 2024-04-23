#src.db.database.py
"""
Database Module.

This module contains the configuration for the database connection,
the session creation, and the base declarative class. It also includes
a function to yield a database session that should be used as a dependency
in FastAPI routes.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from src.conf.config import settings
# Database URL from configuration
DATABASE_URL = settings.sqlalchemy_database_url

# Create engine for database connection
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative class definitions
Base = declarative_base()



# Dependency
def get_db():
    """
    Yield a database session that should be used as a dependency in FastAPI routes.

    This function is a generator that creates a new SessionLocal instance for each request,
    and ensures that the session is closed after the request is finished. This is done using
    Python's context manager (yield statement) and try/finally blocks.

    :yield: A database session.
    :rtype: sqlalchemy.orm.Session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
