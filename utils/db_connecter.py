import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from pymongo import MongoClient

load_dotenv()

def connect_to_mysql(db_name: str):
    """
    This function connects to the given db_name in the MYSQL Database.
    """
    db_user = os.getenv("DB_USERNAME")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    
    try:
        engine = create_engine(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}")
        conn = engine.connect()
        print(f"Connected to Db {db_name}")
        return conn
    except Exception as err:
        print(f"Error {err} occurs while connecting to the database {db_name}")

def connect_to_mongodb(db_name: str):
    """
    This function connects to mongodb database with db_name
    always give db name in uppercase!!
    """
    try:
        client = MongoClient("mongodb://localhost:27017/")
        return client[db_name.upper()]
    except Exception as err:
        print(f"Error {err} occurs while connecting to the database {db_name}")


# client = connect_to_mongodb('CASE_APPOINTMENTS')
# res = client['CASE'].count_documents({})

# print(res)