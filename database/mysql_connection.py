import os
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()

mysql_url = os.getenv("MYSQL_URL")
mysql_db = os.getenv("MYSQL_DB")

engine = create_engine(mysql_url)
connection = engine.connect()
connection.execute(text(f"CREATE DATABASE IF NOT EXISTS {mysql_db}"))
connection.close()

engine = create_engine(mysql_url + "/" + mysql_db)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
