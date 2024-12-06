import hashlib
from app.db_utils import db_client  # Import the MongoDB client utility

# MongoDB configuration
DATABASE_NAME = "VideoGen"
COLLECTION_NAME = "scripts"

def get_unique_filename(base_name):
    """Generates a unique identifier by hashing the input name."""
    hash_object = hashlib.md5(base_name.encode())
    unique_id = hash_object.hexdigest()  # Use the hash as the unique identifier
    return unique_id

def create_project_document(data, base_name):
    """Creates or updates a document in the MongoDB collection."""
    # Generate a unique ID for the document
    unique_id = get_unique_filename(base_name)

    # Add unique ID to the document data
    data["_id"] = unique_id

    # Get the MongoDB collection
    client = db_client.get_client()
    print("Connected to MongoDB")
    collection = client[DATABASE_NAME][COLLECTION_NAME]

    # Insert or update the document in MongoDB
    collection.replace_one({"_id": unique_id}, data, upsert=True)
    print(f"Upsert operation performed for ID: {unique_id}")
    
    return unique_id

def load_project_document(base_name):
    """Loads existing project data from the MongoDB collection."""
    # Generate a unique ID for the document
    unique_id = get_unique_filename(base_name)

    # Get the MongoDB collection
    collection = db_client.get_client()[DATABASE_NAME][COLLECTION_NAME]

    # Retrieve the document from MongoDB
    document = collection.find_one({"_id": unique_id})

    if not document:
        raise ValueError(f"No document found for base name: {base_name}")

    return document

def update_project_document(base_name, data):
    """Updates the document in the MongoDB collection with new data."""
    # Generate a unique ID for the document
    unique_id = get_unique_filename(base_name)

    # Get the MongoDB collection
    collection = db_client.get_client()[DATABASE_NAME][COLLECTION_NAME]

    # Update the document in MongoDB
    collection.update_one({"_id": unique_id}, {"$set": data}, upsert=True)

    return unique_id

