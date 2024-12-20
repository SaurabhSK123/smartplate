import numpy as np
import cv2
import pytesseract as pyt
import os
from io import BytesIO

def detect_plate(img):  
      file_contents = img.read()

      # Convert the file contents to a bytes-like object
      bytes_data = BytesIO(file_contents)

      # Use OpenCV to read the image from the bytes-like object
      img = cv2.imdecode(np.frombuffer(bytes_data.read(), np.uint8), cv2.IMREAD_COLOR)      
      file_path = os.path.join(os.path.dirname(__file__), 'Indianplates.xml')
      car_cascade = cv2.CascadeClassifier(file_path)
      # car_cascade = cv2.CascadeClassifier("./Indianplates.xml")
      # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
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

      #crpped_image = gray[x1:x2+1, y1:y2+1]
      pyt.pytesseract.tesseract_cmd = r'tesseract'
      crpped_image = gray[x1:x2+1, y1:y2+1]
      text = pyt.image_to_string(crpped_image, lang='eng', config='--psm 6')
      x=0
      number = ''
      num = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
      for i in text:
            for j in num:
                  if i == j:
                        number += i
      
      return(number)

