import cv2
import math
import redis
import time
import os
#time.sleep(5)
distance = 0.0
font = cv2.FONT_HERSHEY_SIMPLEX
cap = cv2.VideoCapture(0)
local=""
face_cascade = cv2.CascadeClassifier(local+'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(local+'haarcascade_eye.xml')
r = redis.Redis(host='localhost', port=6379, decode_responses=True)
r.set('distance',0)
while True:
    ret, huge_frame = cap.read()
    frame = cv2.resize(huge_frame, (0,0), fx=0.5, fy=0.5, interpolation=cv2.INTER_NEAREST)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        distancei = (2*3.14 * 180)/(w+h*360)*1000 + 3
        print (distancei)
#        distance = distancei *2.54
        distance = math.floor(distancei/2)* 2.54
        cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
    #cv2.putText(frame,'Distance = ' + str(distance) + 'cm', (5,100),font,1,(0,0,0),2)

    r.set('distance',distance)
    if( 70<=distance):
        print('flag')
        cap.release()
        # Destory the window
        cv2.destroyAllWindows()
        r.set('distance', 0)
        break
 
 
# Stop the capture
cap.release()
# Destory the window
cv2.destroyAllWindows()


