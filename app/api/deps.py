# Common dependencies
from app.db.db import session

def get_db():
    """Dependency to get the database session."""
    db = session()
    try:
        yield db
    finally:
        db.close()
