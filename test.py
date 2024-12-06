from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import time  # Import time module for duration calculation

uri = "mongodb://saarthi:password@localhost:27017"

DATABASE_NAME = "saarthi"
COLLECTION_NAME = "scripts"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
collection = client[DATABASE_NAME][COLLECTION_NAME]

print(collection)
