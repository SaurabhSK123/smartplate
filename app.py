from flask import Flask, render_template, request, redirect, url_for, session , jsonify
from main import app , routes
import cv2
import bcrypt
#from prediction import *
import os


# #return render_template('login.html')

# # Upload Image Data
# @app.route('/success', methods = ['POST'])
# def success():
#     if request.method == 'POST':
#         f = request.files['imagefile']
#         f.save(f.filename)
#         save_path = '/mnt/images'
#         if not os.path.exists(save_path):
#             os.makedirs(save_path)
#         f.save(os.path.join(save_path, f.filename))
#         print('File uploaded Successfully to /mnt/images')
#         img = cv2.imread(f.filename)
#         detect_num = detect_plate(img)
#         info = get_vehicle_info(detect_num)
#         return render_template("result.html",
#                                model = info[0],
#                                regyear = info[1],
#                                engsize = info[2],
#                                sea = info[3],
#                                idfi = info[4],
#                                engnum =  info[5],
#                                fuelt =  info[6],
#                                regdate =  info[7],
#                                loc =  info[8])



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)

