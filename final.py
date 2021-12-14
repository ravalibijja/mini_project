# import necessary packages
import cv2
import pytesseract
import imutils
from PIL import Image
from datetime import datetime
import mysql.connector
# db connect
mydb = mysql.connector.connect(
  host="localhost",
  user="ravali",
  password="root",
  database="ravali"
)
mycursor = mydb.cursor()
mycursor.execute("CREATE TABLE IF NOT EXISTS number_plates (number VARCHAR(255))")
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
image = cv2.imread('red.jpg')
image = imutils.resize(image, 500)
cv2.imshow('Original Image',image)
cv2.waitKey(0)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow('Gray Scale Image', gray)
cv2.waitKey(0)
gray = cv2.bilateralFilter(gray, 11, 17, 17)
cv2.imshow('Smoother image', gray)
cv2.waitKey(0)
edged = cv2.Canny(gray, 170, 200)
cv2.imshow('Canny edge', edged)
cv2.waitKey(0)
cnts, new = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
image1 = image.copy()
cv2.drawContours(image1, cnts, -1, (0,255,0), 3)
cv2.imshow('Canny after contouring', image1)
cv2.waitKey(0)
cnts = sorted(cnts, key=cv2.contourArea, reverse = True)[:30]
NumberPlateCount = None
image2 = image.copy()
cv2.drawContours(image2, cnts, -1, (0,255,0),3)
cv2.imshow('Top 30 contours',image2)
cv2.waitKey(0)
count = 0
name = 1
for i in cnts:
    perimeter = cv2.arcLength(i, True)
    approx = cv2.approxPolyDP(i, 0.02*perimeter, True)
    if(len(approx) == 4):
        NumberPlateCount = approx
        x , y , w , h = cv2.boundingRect(i)
        crp_img = image[y:y+h , x:x+w]
        cv2.imwrite(str(name)+'.png',crp_img)
        name+=1
        break
cv2.drawContours(image, [NumberPlateCount], -1, (0,255,0), 3)
cv2.imshow('Final Image', image)
cv2.waitKey(0)
crop_img_loc = '1.png'
cv2.imshow("Cropped image", cv2.imread(crop_img_loc))
cv2.waitKey(0)
text = pytesseract.image_to_string(crop_img_loc)
print("Number is : ", text)
presentime = datetime.now()
print("  date time :", presentime)
sql = "INSERT INTO number_plates (number) VALUES (%s)"
val = (text)
mycursor.execute(sql, (val,))
mydb.commit()
cv2.waitKey(0)

