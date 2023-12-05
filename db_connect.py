import os
import logging
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


try:
    host_name = os.getenv('HOST_NAME')
    port = os.getenv('PORT')
    db_name = os.getenv('DATABASE_NAME')
    client = MongoClient(host_name,int(port))
    db = client[db_name] 
except Exception as e:
    logging.exception('An exception occurred: %s', e)
    raise ValueError(f"An error occurred while connecting to the database: {e}")