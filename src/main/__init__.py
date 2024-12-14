from flask import Flask
from pymongo import MongoClient

 # Change this to a secure secret key

# MongoDB connection
client = MongoClient("mongodb://0.0.0.0:27017/")
db = client.smartplate
users_collection = db.userdetails
vehicle_collection = db.vehicle_details
location_collection = db.location
owner_collection = db.owner_details
app = Flask(__name__)
app.secret_key = "This is Secret Key" 

from main import routes