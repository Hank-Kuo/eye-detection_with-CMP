import socket
import struct
import time
import pickle
import redis
import cv2
import time
import numpy as np
r = redis.Redis(host='localhost', port=6379)
r1 = redis.Redis(host='140.136.155.36', port=6379, decode_responses=True,password='123456')
r.set('send',"1")
#client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 200]


camera = cv2.VideoCapture(0)

camera.set(3, 500)
camera.set(4, 500)



while True:
    if(r.get('send')==b'1'):
        print("connect")
        #r1.set("data_flag",'open')
        r.set('send','2')
        r1.set("data_flag",'open')
    ret, frame_raw = camera.read()
    img_encode = cv2.imencode('.jpg', frame_raw)[1]
    data_encode = np.array(img_encode)
    str_encode = data_encode.tostring()



    
    #nparr = np.fromstring(str_encode, np.uint8)
    #img_decode = cv2.imdecode(nparr, cv2.IMREAD_COLOR)


    cv2.imshow("f",frame_raw)

    r1.set("data",str_encode)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



    #r1.set("data",data)
    #r1.set("size",size)
    #data=r.get("data")
    #size=int(r.get("size"))
    
    
