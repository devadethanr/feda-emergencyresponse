import pymongo

# Replace with your actual connection details
MONGODB_URI = "mongodb://localhost:27017"
DATABASE_NAME = "fedadb"

client = pymongo.MongoClient(MONGODB_URI)
db = client[DATABASE_NAME]
