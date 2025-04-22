# DB session handling
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
DB_USER = os.getenv('POSTGRES_USER')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD')
DB_HOST = os.getenv('POSTGRES_HOST')
DB_PORT = os.getenv('POSTGRES_PORT')
DB_NAME = os.getenv('POSTGRES_DB')

# Construct the database URL
DB_URL = f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# Create a new SQLAlchemy engine instance
engine = create_engine(DB_URL, echo='debug')    # raw SQL
session = sessionmaker(autocommit=False, autoflush=False, bind=engine) # ORM way

# Define the base model for ORM
Base = declarative_base()