from functools import wraps
from flask import Flask,render_template , jsonify, request, make_response
import requests
from main import app , db
from main.models import *
import jwt
import datetime
app.config['SECRET_KEY'] = 'This is Secret Key'




@app.route('/user/signup', methods=['POST'])
def signup_post():
    data = User()
    return data.signup()

@app.route('/')
def homepage():
   return render_template("login.html")

@app.route('/signup')
def signup_get():
   return render_template("signup.html")

@app.route('/home')
@check_for_token
def admin_page():
   return render_template('home.html')

@app.route('/login',methods=['POST'])
def login_post():
   data = User()
   return data.login()

@app.route('/get_users')
@check_for_token
def getusers():
   data = User()
   resp = data.get_user_list()

   return render_template('user_dash.html',users=resp)


@app.route('/vehicles_dash')
@check_for_token
def vehicle_dash():
   return render_template('vehicle_dash.html')

@app.route('/get_vehicles',methods=['GET'])
@check_for_token
def getvehicles():
   print("HIIII")
   data = User()
   vehicles = data.get_vehicle_list()
   return vehicles

@app.route('/setcookie') 
def setcookie(): 
    
      # Initializing response object 
    resp = make_response('Setting the cookie')  
    resp.set_cookie('GFG','ComputerScience Portal',) 
    return resp 
  
app.run()


