from functools import wraps
from flask import Flask, jsonify,request,Response
import bcrypt
from main import users_collection
import jwt
from datetime import datetime
from datetime import timedelta, datetime
from main  import *

def check_for_token(func):
    @wraps(func)
    def wrapped(*args, **kwargs):

        print(request.cookies)
        token =request.cookies.get('token')
        if not token:
            return jsonify({'result':'missing token'}),403
        try:
            data=jwt.decode(token,app.config['SECRET_KEY'],algorithms=["HS256"])
        except:
            return jsonify({'result':'token invalid'}),403
        return func(*args,**kwargs)
    return wrapped


def create_token(email,password):
        try:
            print("HIIIIIIIIIIIIIII")
            #Check for Username 
            print(email, password)
            if not email:
                # print('in get token',resp_username)
                return jsonify({'WWW-Authenticate':'Basic realm:"login error"'})

            #check for password
            if not password:
                return jsonify({'WWW-Authenticate':'Basic realm:"login error"'})

            print(app.config['SECRET_KEY'])            
            token=jwt.encode({
                'email':email,
                'password':password,
                'exp':datetime.utcnow()+timedelta(weeks=52)},
                app.config['SECRET_KEY']
                )

            return token
        except Exception as e:
            return (jsonify({'WWW-Authenticate':'Basic realm:"login error"'}),e,403)



 


class User:    

    def __init__(self) -> None:
        pass
    # Signup User
    def signup(self):
        try:
            data = request.json
            user = {}
            user['name'] = data['username']
            user['email'] = data['email']
            user['password'] = data['password']
            
            # Salting Password
            salt_rounds = 12  # Adjust this value as needed
            salt = bcrypt.gensalt(rounds=salt_rounds)

            # Hash the password with the generated salt
            hashed_password = bcrypt.hashpw(user['password'].encode('utf-8'), salt)
            user['password'] = hashed_password.decode('utf-8')

            # Check User Exists or Not             
            checkuser = users_collection.find_one({ 'email' :  user['email']})
            
            if checkuser == None:
                users_collection.insert_one(user)
                return jsonify({"status":"success", "message" : "User Added Successfully " })
            else:
                return jsonify({"status":"failed", "message" : "User already Exists "})
        
        except:

            return jsonify({"status":"failed" , "message" : "Server Side Error"})


   # Login User 
    def login(self):
       
       try:
            data = request.json
            user = {}
            user['email'] = data['email']
            user['password'] = data['password']
            
            checkuser = users_collection.find_one({ 'email' :  user['email']},{'_id':0})
            print(checkuser)
            if checkuser == None:
                return jsonify({"status":"failed", "message" : "Username not Registered " })
            
            else:
                hashed_password = checkuser['password']
                print(hashed_password)
                checkpasswd = bcrypt.checkpw(user['password'].encode('utf-8'),hashed_password.encode('utf-8'))
                print(checkpasswd)
                if checkpasswd:
                    print(user['email'],user['password'])
                    token = create_token(user['email'],user['password'])
                   
                    resp = jsonify({"status":"success","name" : checkuser['name'], "username": checkuser['email'] , "staff_status": checkuser['staff_status'], "message" : "Login Succssful "})
                    resp.set_cookie('token', str(token))
                    return resp 

                else:
                    return jsonify({"status":"failed", "message" : "Password not Matched" })


       except:
            
            return  jsonify({"status":"failed", "message" : "Sever Side Error" })
       

    # get_user_list
    def get_user_list(self):
        try:
            user_list = list(users_collection.find({},{'_id':0}))
            return(user_list)
        except Exception as e:
            print(e)
    
    # get locations list
    def get_location_list(self):
        try:
            location_list = list(location_collection.find({},{'_id':0}))
            return(location_list)
        except Exception as e:
            print(e)

    
    # get Vehicle Details
    def get_vehicle_list(self,_data=None):
        print(_data)
        try:
            if _data != None:
                

                current_time = datetime.now()
                vehicle_collection.update_many({'vehicle_no':_data}, {"$set": {"last_datetime": current_time}})
            
                vehicel_list = list(vehicle_collection.find({'vehicle_no': _data },{'_id':0}))
                if vehicel_list == []:
                    vehicel_list = [{'vehicle_no': _data , 'owner_name': 'Unknown', 'owner_licence': '-', 'vehicle_type': '-', 'fine_status': '-', 'status': 'Unauthorised'}]
                    return jsonify({"status":"failed", "message" : "Vehicle is Unauthorised", "data" : vehicel_list })
            else:
                vehicel_list = list(vehicle_collection.find({},{'_id':0}))
            #print(vehicel_list)
            return jsonify ({"status":"success", "message" : "Vehicle is Authorised", "data": vehicel_list  })
    
        except Exception as e:
            print(e)

    # Add Users
    def add_users_data(self):
        try:

            data = request.json
            user = {}
            user['name'] = data['username']
            user['email'] = data['email']
            user['password'] = data['password']
            user['contact'] = data['contact']
            user['staff_status'] = data['staff_status']
            # Salting Password
            salt_rounds = 12  # Adjust this value as needed
            salt = bcrypt.gensalt(rounds=salt_rounds)

            # Hash the password with the generated salt
            hashed_password = bcrypt.hashpw(user['password'].encode('utf-8'), salt)
            user['password'] = hashed_password.decode('utf-8')

            # Check User Exists or Not             
            checkuser = users_collection.find_one({ 'email' :  user['email']})
            
            if checkuser == None:
                users_collection.insert_one(user)
                return jsonify({"status":"success", "message" : "User Added Successfully " })
            else:
                return jsonify({"status":"failed", "message" : "User already Exists "})
        
        except:

            return jsonify({"status":"failed" , "message" : "Server Side Error"})


    # Add Vehicle Details
    def add_vehicles_data(self):
        try:
            vehicles = {}
            data = request.json
            vehicles['vehicle_no'] = data['vehicle_no']
            vehicles['owner_name'] = data['owner_name']
            vehicles['owner_licence'] = data['owner_licence']
            vehicles['vehicle_type'] = data['vehicle_type']
            vehicles['status'] = "Authorized"
            checkvehicle = vehicle_collection.find_one({'vehicle_no' :  vehicles['vehicle_no']})
            
            if checkvehicle == None:
                vehicles['status'] = "Authorized"
                vehicle_collection.insert_one(vehicles)
                return jsonify({"status":"success", "message" : "Vehicle Added Successfully " })
            else:
                return jsonify({"status":"failed", "message" : "Vehicle already Exists "})

        except:    
            return jsonify({"status":"failed" , "message" : "Server Side Error"})

    # Add Location Details
    def add_location_data(self):
        try:
            location = {}
            data = request.json
            location['location_name'] = data['location_name']
            location['area'] = data['area']
            location['city'] = data['city']
            location['state'] = data['state']
            
            checklocation = location_collection.find_one({'location_name' :  location['location_name']})
            
            if checklocation == None:
                location_collection.insert_one(location)
                return jsonify({"status":"success", "message" : "Location Added Successfully " })
            else:
                return jsonify({"status":"failed", "message" : "Location already Exists "})

        except:    
            return jsonify({"status":"failed" , "message" : "Server Side Error"})

    def update_fine_data(self):
        try:
            vehicles = {}
            data = request.json
          
            vehicles_no = data['vehicle_no']
            updated_fine = data['fine_status']
            checkvehicle = vehicle_collection.find_one({'vehicle_no' : vehicles_no})
            if checkvehicle != None:    
              
                vehicle_collection.update_one({"vehicle_no": vehicles_no }, {"$set": {"fine_status": updated_fine}})
                return jsonify({"status":"success", "message" : "Parking Charges Updated " })

            else:
                return jsonify({"status":"failed", "message" : "Vehicle not in Database" })


        except:
            return jsonify({"status":"failed" , "message" : "Server Side Error"})
 

            

    def all_user_page_data(self):
        try:
            data = request.json
            username = data['username']

            owner_details = owner_collection.find_one({ 'email' :  username},{'_id':0})
        
            vehicle_details = vehicle_collection.find_one({'vehicle_no': owner_details['vehicle_no']},{'_id':0})
        
            return jsonify({"status":"success", "owner_details": owner_details , "vehicle_details" : vehicle_details, "message": "data fetched successfully "})
        except:
            return jsonify({"status":"failed" , "message" : "Server Side Error Failed to get details"})


                     



   
    