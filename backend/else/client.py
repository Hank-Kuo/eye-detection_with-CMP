import cv2
import io
import socket
import struct
import time
import pickle
import zlib
from PIL import ImageTk,Image
import numpy as np



client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   
client_socket.connect(('140.136.155.36', 8485))
#140.136.155.133
#192.168.50.146
#140.136.155.36
connection = client_socket.makefile('wb')
cam = cv2.VideoCapture(0)
cam.set(3, 500);
cam.set(4, 500);
img_counter = 0
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 300]
#150 就夠了



while True:
    ret, frame = cam.read()
    result, frame = cv2.imencode('.jpg', frame, encode_param)
    data = zlib.compress(pickle.dumps(frame, 0))
    data = pickle.dumps(frame, 0)
    size = len(data)
    client_socket.sendall(struct.pack(">L", size) + data)
    


cam.release()
cam.release()