import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

db_url = os.getenv(db_url)
engine = create_engine(db_url)
session = sessionmaker(autoflush=False,bind=engine,autocommit=False)