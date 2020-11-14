from tkinter import *
from PIL import ImageTk,Image
import redis
import random
import time
import datetime
import numpy as np
import threading
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os
import cv2
import io
import socket
import struct
import time
import pickle
import zlib
import math


local=""



r = redis.Redis(host='localhost', port=6379, decode_responses=True)
r.set("video",'client')






#socket 
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
img_counter = 0
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 200]


cam = cv2.VideoCapture(0)
def video_loop():
    global cam
    global client_socket
    if(r.get('video')== 'client' ):
        client_socket.connect(('140.136.155.36', 8485))
        connection = client_socket.makefile('wb')
        cam.set(3, 500);
        cam.set(4, 500);
        r.set('video','client1')
    elif(r.get('video')=='client1'):
        ret, frame_raw = cam.read()
        result, frame = cv2.imencode('.jpg', frame_raw, encode_param)
#    data = zlib.compress(pickle.dumps(frame, 0))
        data = pickle.dumps(frame, 0)
        size = len(data)
        client_socket.sendall(struct.pack(">L", size) + data)
        cv2image = cv2.cvtColor(frame_raw, cv2.COLOR_BGR2RGBA)#转换颜色从BGR到RGBA
        current_image = Image.fromarray(cv2image)#将图像转换成Image对象
        imgtk = ImageTk.PhotoImage(image=current_image)
        panel.imgtk = imgtk
        panel.config(image=imgtk)
    root.after(1,video_loop)
















# tkinter setting 
root = Tk()
root.attributes("-fullscreen",True)
root.configure(background='white')
img = ImageTk.PhotoImage(Image.open(local+'E/teststarting.png'))
tkimg=Label(root,image = img)
tkimg.place(relx=.5, rely=.5,anchor="center")


#camera
panel = Label(root)  # initialize image panel
panel.place(x = 0,y=0)
video_loop()
root.mainloop()