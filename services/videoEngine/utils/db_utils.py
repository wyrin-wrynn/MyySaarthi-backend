import hashlib
from db_utils import db_client  # Import the MongoDB client utility
import os

# MongoDB configuration
DATABASE_NAME = os.getenv("DATABASE_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

def get_unique_filename(base_name):
    """Generates a unique identifier by hashing the input name."""
    hash_object = hashlib.md5(base_name.encode())
    unique_id = hash_object.hexdigest()  # Use the hash as the unique identifier
    return unique_id

def create_project_document(data):
    """Creates or updates a document in the MongoDB collection."""
    # Generate a unique ID for the document
    unique_id = get_unique_filename(data["url"])

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

def getDrafts():
    # Get the MongoDB collection
    client = db_client.get_client()
    collection = client[DATABASE_NAME][COLLECTION_NAME]
    drafts = collection.find({"status":"wip"})
    print(drafts)
    draft_projects = []
    for draft in drafts:
        temp = {}
        temp['id'] = draft['_id']
        temp['imageUrl'] = draft['image_url']
        temp['currentStep'] = draft['current_step']
        temp['title'] = draft['title']
        draft_projects.append(temp)
    print(draft_projects)
    return draft_projects

def getProjectDraft(project_id):
    from bson import ObjectId  # To handle MongoDB ObjectId
    
    # Get the MongoDB collection
    client = db_client.get_client()
    collection = client[DATABASE_NAME][COLLECTION_NAME]

    try:
        # Query the collection for the project with the given id
        project = collection.find_one({"_id": project_id})

        if not project:
            return {"error": "Project not found"}, 404


        return project, 200

    except Exception as e:
        print(f"Error fetching project draft: {e}")
        return {"error": "An error occurred while fetching the project draft"}, 500
