import numpy as np
import requests
import cv2
import pytesseract as pyt
from PIL import Image
import xmltodict
import json

def detect_plate(img):
      car_cascade = cv2.CascadeClassifier("./templates/Indianplates.xml")
      gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
      if img is not None:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            cars = car_cascade.detectMultiScale(gray, 1.1, 50)
            image_filter = cv2.bilateralFilter(gray, 11, 17, 17)
            edge = cv2.Canny(image_filter, 30, 200)
            for (x,y,w,h) in cars:
                  location = np.array([[[x+w,y]],[[x,y]],[[x,y+h]],[[x+w,y+h]]])
                  mask = np.zeros(gray.shape, np.uint8)
                  new_image = cv2.drawContours(mask, [location], 0, 255, -1)
                  new_image = cv2.bitwise_and(img, img, mask=mask)
      else:
            return("No Plate recognized")

      (x,y) = np.where(mask==255)
      (x1,y1) = (np.min(x), np.min(y))
      (x2,y2) = (np.max(x), np.max(y))

      crpped_image = gray[x1:x2+1, y1:y2+1]
      pyt.pytesseract.tesseract_cmd = r'tesseract'
      text = pyt.image_to_string(crpped_image, lang='eng', config='--psm 6')
      x=0
      number = ''
      num = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
      for i in text:
            for j in num:
                  if i == j:
                        number += i
      print(number)
      return(number)

def get_vehicle_info(plate_number):
    r = requests.get("http://www.regcheck.org.uk/api/reg.asmx/CheckIndia?RegistrationNumber={0}&username=vikas@123".format(str(plate_number)[:10]))
    data = xmltodict.parse(r.content)
    jdata = json.dumps(data)
    df = json.loads(jdata)
    df1 = json.loads(df['Vehicle']['vehicleJson'])
    return [df1["Description"],
           df1["RegistrationYear"],
           df1["EngineSize"]["CurrentTextValue"],
           df1["NumberOfSeats"]["CurrentTextValue"],
           df1["VechileIdentificationNumber"],
           df1["EngineNumber"],
           df1["FuelType"]["CurrentTextValue"],
           df1["RegistrationDate"],
           df1["Location"]]