import redis
import socket 
import cv2
    elif(r.get('video')=='client1'):
        ret, frame_raw = camera.read()
        result, frame = cv2.imencode('.jpg', frame_raw, encode_param)
        #data = zlib.compress(pickle.dumps(frame, 0))
        data = pickle.dumps(frame, 0)
        size = len(data)
    elif(r.get('video')=='client1'):
        ret, frame_raw = camera.read()
        result, frame = cv2.imencode('.jpg', frame_raw, encode_param)
        #data = zlib.compress(pickle.dumps(frame, 0))
        data = pickle.dumps(frame, 0)
        size = len(data)
        r.set("data",data)
        r.set("size",size)
        #client_socket.sendall(struct.pack(">L", size) + data)
        color =(0,0,0)  #red  (0,0,255)    (0,255,0)
        if(str(r.get("gesture_flag"))=="move"):
            color=(0,255,0)
        else:
            color=(0,0,255)
        frame_raw = cv2.resize(frame_raw, (300, 300))
        cv2.rectangle(frame_raw,(100,50),(200,150),color,5)
        frame_raw = cv2.flip(frame_raw,1)
        cv2image = cv2.cvtColor(frame_raw, cv2.COLOR_BGR2RGBA)#转换颜色从BGR到RGBA
        current_image = Image.fromarray(cv2image)#将图像转换成Image对象
        imgtk = ImageTk.PhotoImage(image=current_image)
        panel.imgtk = imgtk
        panel.config(image=imgtk)