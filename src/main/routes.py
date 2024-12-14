from functools import wraps
from flask import render_template , jsonify, request, make_response
import requests
from main import app , db
from main.models import *
from .prediction import *
app.config['SECRET_KEY'] = 'This is Secret Key'




@app.route('/ping',methods=['GET'])
def ping():
    data = { "ping" : "pong" }
    return data
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

@app.route('/all_user_page_data', methods=['POST'])
@check_for_token
def all_page_data():
   data = User()
   page_data = data.all_user_page_data()
   return page_data

@app.route('/home')
@check_for_token
def admin_page():
   return render_template('home.html')

@app.route('/user')
@check_for_token
def user_page():
   return render_template('users.html')

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

@app.route('/add_cctv')
@check_for_token
def get_cctv_page():
   return render_template('cctv.html')

@app.route('/get_live')
@check_for_token
def get_live():
   return render_template('live.html')



@app.route('/vehicles_dash')
@check_for_token
def vehicle_dash():
   return render_template('vehicle_dash.html')



@app.route('/get_vehicles',methods=['POST'])
@check_for_token
def getvehicles():
   data = User()
   vehicles = data.get_vehicle_list()
   return vehicles



@app.route('/setcookie') 
def setcookie(): 
    
      # Initializing response object 
    resp = make_response('Setting the cookie')  
    resp.set_cookie('GFG','ComputerScience Portaal',) 
    return resp 



@app.route('/logout')
def logout():
    resp = make_response(render_template('login.html'))
    resp.headers['Clear-Session-Storage'] = 'true' 
    resp.set_cookie('token',expires=0)
    return  resp




# @app.route('/logout')
# def logout():
#     # Create a response to render the login page
#     resp = make_response(jsonify(message="Logged out successfully"))
#     resp.set_cookie('token', '', expires=0)  # Remove the token cookie
#     resp.headers['Clear-Session-Storage'] = 'true'  # Set a header to clear session storage
#     return resp


@app.route('/add_users',methods=['POST'])
@check_for_token
def add_users():
    data = User()
    return data.add_users_data()

@app.route('/add_vehicles',methods=['POST'])
@check_for_token
def add_vehicles():
   data = User()
   return data.add_vehicles_data()

@app.route('/anpr_cam')
@check_for_token
def anpr_home():
   return render_template('anpr_home.html')


@app.route('/locations')
@check_for_token
def location():
   return render_template('location.html')
   

@app.route('/get_location')
@check_for_token
def get_location():
    data = User()
    return data.get_location_list() 


@app.route('/add_location',methods=['POST'])
@check_for_token
def add_location():
    data = User()
    return data.add_location_data()

@app.route('/update_fine', methods=['POST'])
@check_for_token
def update_fine():
   fine_data = User()
   return fine_data.update_fine_data()




@app.route('/uploadandget',methods=['POST'])
@check_for_token
def upload_and_get():
   
   if 'file' not in request.files:
      return jsonify({"status":"failed", "message" : " No file part" }), 400

   file = request.files['file']
   
    # Check if the file is empty
   if file.filename == '':
      return jsonify({'status': "failed", "message": 'No selected file'}), 400\
      
   no_plate = detect_plate(file)
   print(no_plate)
   user= User()
   v_list = user.get_vehicle_list(_data=no_plate)
   return v_list
      











