from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import atexit
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class MongoDBClient:
    def __init__(self, uri):
        self.uri = uri
        self.client = None

    def connect(self):
        """Establish connection to MongoDB."""
        if not self.client:
            self.client = MongoClient(self.uri, server_api=ServerApi('1'))
            try:
                self.client.admin.command('ping')
                print("Successfully connected to MongoDB!")
            except Exception as e:
                print(f"Failed to connect to MongoDB: {e}")
                self.client = None

    def get_client(self):
        """Get the MongoDB client. Automatically connects if not already connected."""
        if not self.client:
            self.connect()
        return self.client

    def close(self):
        """Close the MongoDB connection."""
        if self.client:
            self.client.close()
            print("MongoDB connection closed.")
            self.client = None


# Get MongoDB URI from .env file
MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError("MONGO_URI is not set in the .env file")

# Create a singleton MongoDB client instance
db_client = MongoDBClient(MONGO_URI)

# Register the close method to be called on exit
atexit.register(db_client.close)
