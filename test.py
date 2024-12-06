from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import time  # Import time module for duration calculation

uri = "mongodb+srv://saarthi:bitsgoa123@dev.urisn.mongodb.net/?retryWrites=true&w=majority&appName=Dev"

DATABASE_NAME = "VideoGen"
COLLECTION_NAME = "scripts"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
collection = client[DATABASE_NAME][COLLECTION_NAME]

# Start time
start_time = time.time()

print("running query now")
docs = collection.find({"aspect": "Portrait"})

print("got results")

for doc in docs:
    print("Entered loop")
    aspect = doc['aspect']
    print(aspect)

# End time
end_time = time.time()

# Calculate duration
duration = end_time - start_time
print(f"Execution time: {duration:.2f} seconds")
