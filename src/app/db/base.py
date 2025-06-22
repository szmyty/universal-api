from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """Base class for all database models."""
    __abstract__ = True  # This ensures that SQLAlchemy does not create a table for this class
    pass
