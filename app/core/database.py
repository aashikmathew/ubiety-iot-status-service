from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Get the database URL from environment or use default for Docker Compose
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://ubiety:password@db:5432/ubiety_iot")

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class for DB sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)