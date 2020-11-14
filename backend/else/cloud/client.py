import cv2
import io
import socket
import struct
import time
import pickle
import zlib
from tkinter import *
from PIL import ImageTk,Image
import numpy as np
import threading

from multiprocessing import Process

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.50.46', 8485))
#140.136.155.133
#192.168.50.146
#140.136.155.36
connection = client_socket.makefile('wb')
cam = cv2.VideoCapture(0)
cam.set(3, 500);
cam.set(4, 500);
img_counter = 0
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 10]
flag=0
a=0


while True:
    ret, frame = cam.read()
    result, frame = cv2.imencode('.jpg', frame, encode_param)
#    data = zlib.compress(pickle.dumps(frame, 0))
    data = pickle.dumps(frame, 0)
    size = len(data)
    client_socket.sendall(struct.pack(">L", size) + data)
    img_counter += 1
'''   
    p=threading.Thread(target=client(client_socket))
    p.start()
    
'''
'''
    if(client_socket.recv(1024)):
        gesture=client_socket.recv(1024)
        if(gesture==b'one' and flag!=1):
            print('one')
            p=threading.Thread(target=save('1'))
            p.start()
            flag=1
        if(gesture==b'two' and flag!=2):
            print('two')
            flag=2

            p=threading.Thread(target=save('2'))
            p.start()


        if(gesture==b'three' and flag!=3):
            print('three')
            flag=3
            p=threading.Thread(target=save('3'))
            p.start()

        if(gesture==b'four' and flag!=4):
            print('four')
            flag=4
            p=threading.Thread(target=save('4'))
            p.start()
        if(gesture==b'five' and flag!=5):
            print('five')
            flag=5
            p=threading.Thread(target=save('5'))
            p.start()
'''


cam.release()