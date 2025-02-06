from pymongo import MongoClient

db_username = ""
db_password = ""
MONGO_URI = f"mongodb+srv://{db_username}:{db_password}@cluster0.eccom.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(MONGO_URI)

db = client["ai_agora"]

user_collection = db["user"]
object_collection = db["object"]
debate_collection = db["debate"]