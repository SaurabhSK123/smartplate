from flask import Flask
from pymongo import MongoClient

 # Change this to a secure secret key

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client.smartplate
users_collection = db.userdetails
vehicle_collection = db.vehicle_details
location_collection = db.location
app = Flask(__name__)
app.secret_key = "your_secret_key" 

from main import routes