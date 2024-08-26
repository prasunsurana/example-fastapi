from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

import psycopg2 # default postgres driver
from psycopg2.extras import RealDictCursor
import time

SQLALCHEMY_DATABASE_URL = f'''postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'''
# hardcoding is bad practice

engine = create_engine(SQLALCHEMY_DATABASE_URL)
# If you are using sqlite, add another argument to the above: connect_args={'check_same_thread':False}
# This is not needed for postgres.

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# CONNECTING TO SQL DIRECTLY RATHER THAN USING ORM LIKE SQLALCHEMY

# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', 
#                                 password='hajmola28', cursor_factory=RealDictCursor)
        
#         cursor = conn.cursor()
#         print('Database connection was successful!')
#         break
#     except Exception as error:
#         print('Connecting to database failed')
#         print(f'Error = {error}')
#         time.sleep(3)
