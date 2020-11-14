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

# 位置
local=os.path.abspath('.').replace("\\","/")+"/code/"
#os.path.abspath('.').replace("\\","/")+"/code/"

# 測驗變數
count=0 # 紀錄次數
mistake=0 # 錯誤
level=0
pic=''
k=[local+'E/0.1',local+'E/0.2',local+'E/0.4',local+'E/0.6',local+'E/0.8',local+'E/1.0',local+'E/2.0'] # 圖片名稱
k1=['.png',' – 1.png',' – 2.png',' – 3.png'] # 圖片名稱2
flag='right' # reco left or right  
#flag={'flag_eye':'right',}
choices = [0,1,2,3] # 隨機變數
avg=1/4  # 機率
de=0.3 # 機率
de1=0.1 #機率
weights = [avg,avg,avg,avg] # 測驗權重

#對應之變數
gesture_co={'right':0,'down':1,'left':2,'up':3,'cycle':4}   #視力測驗
gesture_co_1={'up':"沒有",'cycle':"有"} # flash and blind 
gesture_co_2={'up':"有",'cycle':"沒有"} # mosqito and yellow
coor={"-1":"0.1","0":"0.2","1":"0.4","2":"0.6","3":"0.8","4":"1.0","5":"2.0"} # 對應之度數


coor_score={"0.1-0.3":"Worst","0.4-0.7":"Bad","0.8-1.1":"Good", "1.2-1.5":"Nice","1.5-2.0":"Excellent"} # 判別好壞
coor_recom={"Worst":"建議去看醫生","Bad":"建議去看醫生","Good":"請少用3C產品","Nice":"請繼續保持","Excellent":"請繼續保持"} # 推薦看醫生與否


''' 
0.1-0.3 => Worst 
0.4-0.7 => bad 
0.8-1.1 => good 
1.2-1.5 => nice 
1.5-2.0 => Excellent 

if is bad or worst  => see doctor
if is good => less use 3C product 
if is Nice or Excellent => keep going 

'''

#node js with python connect 
f = open(local+"email.txt", "r")
email=f.readline()

# redis connect 
r = redis.Redis(host='localhost', port=6379, decode_responses=True)
r1 = redis.Redis(host='140.136.155.36', port=6379,password='123456')



# firebase 基本設定
cred = credentials.Certificate(local+'serviceAccount.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
eye_tem= db.collection(u'User').document(u''+email)  # user 
eye_temp=eye_tem.get().to_dict()["eye_temp"]  # eye_temp
number=(int(eye_temp[-1:])+1)%4 # temp number
if(number==0):
    number+=1
eye_temp=eye_temp[0:-1]+str(number)
eye_tem.update({u'eye_temp': eye_temp})
user_info= db.collection(u'User').document(u''+email).collection(u'eyesight').document(u''+eye_temp)
doc={}




# distance 
face_cascade = cv2.CascadeClassifier(local+'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(local+'haarcascade_eye.xml')
distance = 0.0
font = cv2.FONT_HERSHEY_SIMPLEX
r.set('video','distance')


# 將影像嵌入tkinter 
def video_loop():
    global distance 
    global huge_frame
    global client_socket
    global camera
    if(r.get('video')=='distance'):  # 開關
        success, huge_frame = camera.read() # 影像
        frame = cv2.resize(huge_frame, (0,0), fx=0.5, fy=0.5, interpolation=cv2.INTER_NEAREST) # resize 
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #灰階
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            distancei = (2*3.14 * 180)/(w+h*360)*1000 + 3 
            print (distancei)
            distance = math.floor(distancei/2)* 2.54 # 距離計算
            r.set('distance',distance) #距離載入redis
            cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2) # 矩形
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_gray) # 偵測人臉
            for (ex,ey,ew,eh) in eyes:
                cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
        cv2.waitKey(1)
        frame = cv2.flip(frame,1) # 翻轉
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)#转换颜色从BGR到RGBA
        current_image = Image.fromarray(cv2image)#将图像转换成Image对象
        imgtk = ImageTk.PhotoImage(image=current_image)
        panel.imgtk = imgtk
        panel.config(image=imgtk)
    elif(r.get('video')=='client'):
        camera.release() # 關閉影像
        r.set('video','client2')
    elif(r.get('video')=='client2'):
        camera = cv2.VideoCapture(0) #測驗影像
        #camera.set(3, 500)
        #camera.set(4, 500)
        r.set('video','client1') # 開關設定
        r1.set("data_flag","open") # 開關設定
        print("connect")
        #r.set('send','1')
    elif(r.get('video')=='client1'):
        ret, frame_raw = camera.read()
        '''
        result, frame = cv2.imencode('.jpg', frame_raw, encode_param)
        data = zlib.compress(pickle.dumps(frame, 0))
        data = pickle.dumps(frame, 0)
        size = len(data)
        r.set("size",size) 
        client_socket.sendall(struct.pack(">L", size) + data)
        '''
        print("send")
        img_encode = cv2.imencode('.jpg', frame_raw)[1] # 編碼
        data_encode = np.array(img_encode)
        str_encode = data_encode.tostring()
        r1.set("data",str_encode) # 傳入server 
        color =(0,0,0)  #red  (0,0,255)    (0,255,0)  # 設定顏色
        if(str(r.get("gesture_flag"))=="move"):
            color=(0,255,0)
        else:
            color=(0,0,255)
        frame_raw = cv2.resize(frame_raw, (300, 300),interpolation=cv2.INTER_NEAREST)
        cv2.rectangle(frame_raw,(100,50),(200,150),color,5)  # 矩形顯示
        frame_raw = cv2.flip(frame_raw,1)
        cv2image = cv2.cvtColor(frame_raw, cv2.COLOR_BGR2RGBA)#转换颜色从BGR到RGBA
        current_image = Image.fromarray(cv2image)#将图像转换成Image对象
        imgtk = ImageTk.PhotoImage(image=current_image)
        panel.imgtk = imgtk
        panel.config(image=imgtk)
    root.after(1,video_loop)









# tkinter intial 
root = Tk()
root.attributes("-fullscreen",True) # 全螢幕
root.configure(background='white') #背景
tkimg=Label(root,image = "")
B = Button(root,image = "" )

# 螢幕尺寸按鈕取消
def inti():
    size_1.destroy()
    size_2.destroy()
    size_3.destroy()
    img = ImageTk.PhotoImage(Image.open(local+'E/teststarting.png'))
    photo1 = Image.open(local+'E/skip_button.png')
    phot=photo1.resize((200, 100),Image.ANTIALIAS)
    phot=ImageTk.PhotoImage(phot)
    #tkimg=Label(root,image = img)
    tkimg.configure(image=img)
    tkimg.image =img
    tkimg.place(relx=.5, rely=.5,anchor="center")
    #B = Button(root ,image=phot,bg="white")
    B.configure(image=phot)
    B.image =phot
    B.place(relx=0.86, rely=0.07)
    tkimg.after(100, model_distance_0)


# 設定螢幕尺寸按鈕15
photo1 = Image.open(local+'E/screen15.png')
phot_1=photo1.resize((300, 300),Image.ANTIALIAS)
phot_1=ImageTk.PhotoImage(phot_1)
# 設定螢幕尺寸按鈕24
photo2 = Image.open(local+'E/screen24.png')
phot_2=photo2.resize((300, 300),Image.ANTIALIAS)
phot_2=ImageTk.PhotoImage(phot_2)
# 設定螢幕尺寸按鈕27
photo3 = Image.open(local+'E/screen27.png')
phot_3=photo3.resize((300, 300),Image.ANTIALIAS)
phot_3=ImageTk.PhotoImage(phot_3)

# 設定螢幕尺寸按鈕
size_2= Button(root ,text="電腦尺寸 : 11 ",bg="white", command = inti, image=phot_2) # command 執行動作
size_3= Button(root ,text="電腦尺寸 : 15 ",bg="white", command = inti, image=phot_3)
size_2.place(relx=.5, rely=.5,anchor="center")
size_3.place(relx=.8, rely=.5,anchor="center")
size_1= Button(root ,text="電腦尺寸 : 13 ",bg="white", command = inti, image=phot_1)
size_1.place(relx=.2, rely=.5,anchor="center")


#camera
camera = cv2.VideoCapture(0)
panel = Label(root)  # initialize image panel
panel.place(x = 0,y=0)
video_loop()
var={'pic':'','mistake':'','count':'','level':''}




global flag_show
eye_flag=False
# 視力測驗_1
def model():
    global pic
    global mistake
    global count
    global level
    global flag
    global choices
    global avg
    global de
    global de1
    global weights
    global rn
    global mistake
    global eye_flag
    if(mistake!=2 and count!=3 and eye_flag==False):
        #測三次
        rn = np.random.choice(choices, p=weights) # 設定權重
        index=choices.index(rn)
        weights=[de,de,de,de] # 權重
        weights[index]=de1 # 權重
        pic=k[level]+k1[rn] # 圖片
        count += 1
        bm1 = ImageTk.PhotoImage(Image.open(pic)) # 開啟圖片
        tkimg.configure(image=bm1) # 改變圖片
        tkimg.image = bm1
        print(rn)
        #var[pic]=pic
        #var[mistake]=mistake
        #var[count]=count
        #var[level]=level
        print('pic :', pic + " mistake", mistake, ' count', count, ' level', level)
        #eye_flag=True
        tkimg.after(1200, modelll) # 跳轉
    elif(count==3 and mistake!=2 and level!=6):
        #對兩個 下一個LEVEL
        level+=1
        count=0
        mistake=0
        tkimg.after(20, model)
    elif((mistake==2 or level ==6)  and flag=='right'):
        # change to left and save right info
        flag='left'
        print(str(level-1))
        level_1=coor[str(level-1)]
        doc['left']=level_1
        print('left eye is ',level-1)
        print('turn cover left eye')
        count=0
        level=0
        mistake=0
        tkimg.after(200, model_left_eye)
    elif ((mistake == 2 or level == 6)  and flag == 'left'):
        # change to flash and save left info
        level_1=coor[str(level-1)]
        doc['right']=level_1
        bm1 = ImageTk.PhotoImage(Image.open(local + 'E/通通遮起來.png'))
        tkimg.configure(image=bm1)
        print('right eye is ',level - 1)
        count = 0
        mistake=0
        tkimg.after(200, model_flash)
        #root.destroy()

# 視力測驗_2
def modelll():
    #Double show image
    global mistake
    global set_text
    global eye_flag
    eye_flag=True
    bm1 = ImageTk.PhotoImage(Image.open(pic))
    tkimg.configure(image=bm1)
    tkimg.image = bm1
    gesture = str(r.get('gesture'))
    destion= modelll
    if(gesture=="up" or gesture == "down" or gesture=='left' or gesture=="right" or gesture=="cycle" ):  # 判斷手勢是否符合
        gesture_reco=gesture_co[gesture]
        set_text="E/test.png" # 圖片正確與否
        if (gesture_reco != rn and gesture_reco!=4):
            print('wrong')
            mistake += 1
            set_text="E/wrong.png"
        elif(gesture_reco==4):
            mistake += 1
            set_text="E/pass.png"
        eye_flag=False
        destion=modell1_show_mistake
    tkimg.after(100, destion)

# show the right answer or wrong answer 
def modell1_show_mistake():
    global set_text
    bm1 = ImageTk.PhotoImage(Image.open(local+set_text))
    tkimg.configure(image=bm1)
    tkimg.image = bm1
    tkimg.after(1000, model)




# show teststarting  一開始測驗介紹
def model_distance_0():
    bm1 = ImageTk.PhotoImage(Image.open(local+'E/teststarting.png'))
    tkimg.configure(image=bm1)
    tkimg.image = bm1
    r.set('flag_sound',12)
    tkimg.after(200, model_distance_00)

# show teststarting    control sound 
def model_distance_00():
    bm1 = ImageTk.PhotoImage(Image.open(local+'E/teststarting.png'))
    tkimg.configure(image=bm1)
    tkimg.image = bm1
    dest=model_distance_00
    if(int(r.get("flag_sound"))!=12):
        dest=model_gesture_description
    tkimg.after(200,dest)

#手勢規則
def model_gesture_description():
    bm1 = ImageTk.PhotoImage(Image.open(local+'E/description.png'))
    tkimg.configure(image=bm1)
    tkimg.image = bm1
    r.set('flag_sound',9)
    tkimg.after(200,model_gesture_description_1)
def model_gesture_description_1():
    bm1 = ImageTk.PhotoImage(Image.open(local+'E/description.png'))
    tkimg.configure(image=bm1)
    tkimg.image = bm1
    dest=model_gesture_description_1
    if(int(r.get("flag_sound"))!=9):
        dest=model_gesture_up
    tkimg.after(200,dest)

# 手勢介紹
def model_gesture_up():
    bm1 = ImageTk.PhotoImage(Image.open(local+'E/hand_up.png'))
    tkimg.configure(image=bm1)
    tkimg.image = bm1
    tkimg.after(3000,model_gesture_down)
def model_gesture_down():
    bm1 = ImageTk.PhotoImage(Image.open(local+'E/hand_down.png'))
    tkimg.configure(image=bm1)
    tkimg.image = bm1
    tkimg.after(3000,model_gesture_left)
def model_gesture_left():
    bm1 = ImageTk.PhotoImage(Image.open(local+'E/hand_left.png'))
    tkimg.configure(image=bm1)
    tkimg.image = bm1
    tkimg.after(3000,model_gesture_right)
def model_gesture_right():
    bm1 = ImageTk.PhotoImage(Image.open(local+'E/hand_right.png'))
    tkimg.configure(image=bm1)
    tkimg.image = bm1
    tkimg.after(3000,model_gesture_fist)
def model_gesture_fist():
    bm1 = ImageTk.PhotoImage(Image.open(local+'E/hand_fist.png'))
    tkimg.configure(image=bm1)
    tkimg.image = bm1
    tkimg.after(3000,model_distance)

# show distance 
def model_distance():
    bm1 = ImageTk.PhotoImage(Image.open(local+'E/distancehint.png'))
    tkimg.configure(image=bm1)
    tkimg.image = bm1
    r.set('flag_sound',1)
    B.destroy()
    tkimg.after(200, model_distance_1)

# control sound
def model_distance_1():
    bm1 = ImageTk.PhotoImage(Image.open(local+'E/distancehint.png'))
    tkimg.configure(image=bm1)
    tkimg.image = bm1
    dest=model_distance_1
    if(int(r.get("flag_sound"))!=1):
        dest=model_distance_2
        #r.set('video','client')
    tkimg.after(200,dest)

def model_distance_2():
    bm1 = ImageTk.PhotoImage(Image.open(local+'E/distancehint.png'))
    tkimg.configure(image=bm1)
    tkimg.image = bm1
    dest=model_distance_1
    if(float(r.get('distance'))>50):
        dest=model_right_eye
        r.set('video','client')
    tkimg.after(200,dest)
'''
    if(float(r.get('distance'))>70):
        #r.set('flag_distance','false')
        #r.set('flag_cpm','true')
        tkimg.after(200, model_empty)
    tkimg.after(2000, model_right_eye)
def show_hand():
	bm1 = ImageTk.PhotoImage(Image.open(local+'E/distancehint.png'))
    tkimg.configure(image=bm1)
    tkimg.image = bm1
    dest=model_distance_1
'''


#cover 右眼  
def model_right_eye():
    bm1 = ImageTk.PhotoImage(Image.open(local+'E/coverrighteye.png'))
    tkimg.configure(image=bm1)
    tkimg.image = bm1
    r.set('video','client')
    r.set('flag_sound',10)
    tkimg.after(200, model_right_eye_1)
 # control sound  
def model_right_eye_1():
    bm1 = ImageTk.PhotoImage(Image.open(local+'E/coverrighteye.png'))
    tkimg.configure(image=bm1)
    tkimg.image = bm1
    dest=model_right_eye_1
    if(int(r.get("flag_sound"))!=10):
        dest=model_empty
    tkimg.after(200, dest)


#cover左眼  
def model_left_eye():
    bm1 = ImageTk.PhotoImage(Image.open(local+'E/coverlefteye.png'))
    tkimg.configure(image=bm1)
    tkimg.image = bm1
    r.set('flag_sound',11)
    tkimg.after(200, model_left_eye_1)
 # control sound  
def model_left_eye_1():
    bm1 = ImageTk.PhotoImage(Image.open(local+'E/coverlefteye.png'))
    tkimg.configure(image=bm1)
    tkimg.image = bm1
    dest=model_left_eye_1
    if(int(r.get("flag_sound"))!=11):
        dest=model_empty
    tkimg.after(200,dest)




# sometiome will fail so need to show the empty to cover the 
def model_empty():
    bm1 = ImageTk.PhotoImage(Image.open(local+'E/通通遮起來.png'))
    tkimg.configure(image=bm1)
    tkimg.image = bm1
    tkimg.after(20, model)




# flash test 
flag_flash=0
def model_flash():
    global flag_flash
    if(flag_flash==0):
        bm1 = ImageTk.PhotoImage(Image.open(local+'E/flash.png'))
        tkimg.configure(image=bm1)
        tkimg.image = bm1 
        flag_flash+=1
        tkimg.after(2000, model_flash)
    elif(flag_flash==1):
        bm1 = ImageTk.PhotoImage(Image.open(local + 'E/flash_guard.png'))
        tkimg.configure(image=bm1)
        tkimg.image = bm1
        flag_flash+=1
        r.set("flag_sound",4)
        tkimg.after(20, model_flash)
    elif (flag_flash == 2):
        bm1 = ImageTk.PhotoImage(Image.open(local + 'E/flash_guard.png')) # 說明測驗
        tkimg.configure(image=bm1)
        tkimg.image = bm1
        if(int(r.get("flag_sound"))!=4):
            flag_flash += 1
        tkimg.after(2000, model_flash)
    elif (flag_flash == 3):
        bm1 = ImageTk.PhotoImage(Image.open(local + 'E/coverrighteye.png')) # 遮右眼
        tkimg.configure(image=bm1)
        tkimg.image = bm1
        flag_flash += 1
        tkimg.after(2000, model_flash)
    elif(flag_flash == 4 or flag_flash==8):
        bm1 = ImageTk.PhotoImage(Image.open(local +'E/flash_test.jpg')) # 測驗圖片
        tkimg.configure(image=bm1)
        tkimg.image = bm1
        flag_flash += 1
        tkimg.after(1500, model_flash)
    elif(flag_flash == 5 or flag_flash==9):
        bm1 = ImageTk.PhotoImage(Image.open(local + 'E/flash_test.jpg'))# 測驗圖片
        tkimg.configure(image=bm1)
        tkimg.image = bm1
        gesture = str(r.get('gesture'))
        print(gesture)
        if(gesture=="up" or gesture=="cycle"): # 接收手勢
            gesture_reco=gesture_co_1[gesture] 
            print(gesture_reco)
            if(flag_flash == 5): 
                doc['flash_left'] = gesture_reco # 載入測驗結果
                print('left'+gesture)
            else:
                doc['flash_right'] = gesture_reco# 載入測驗結果
                print('right' + gesture)
            flag_flash += 1
            print(flag_flash)
            if(flag_flash==10):
                tkimg.after(200, model_color_bindness)# 跳至下一測驗
        tkimg.after(200, model_flash)

    elif(flag_flash==6):
        bm1 = ImageTk.PhotoImage(Image.open(local + 'E/通通遮起來.png'))
        tkimg.configure(image=bm1)
        tkimg.image = bm1
        flag_flash+=1
        tkimg.after(20, model_flash)

    elif(flag_flash==7):
        bm1 = ImageTk.PhotoImage(Image.open(local + 'E/coverlefteye.png')) # 左眼
        tkimg.configure(image=bm1)
        tkimg.image = bm1
        flag_flash += 1
        tkimg.after(2000, model_flash)





# color bindness 
flag_blind=0
def model_color_bindness():
    global  flag_blind
    if(flag_blind==0):
        bm1 = ImageTk.PhotoImage(Image.open(local + 'E/color_blind.png')) # 說明測驗1
        tkimg.configure(image=bm1)
        tkimg.image = bm1
        flag_blind+=1
        tkimg.after(2000, model_color_bindness)
    elif(flag_blind==1):
        bm1 = ImageTk.PhotoImage(Image.open(local + 'E/number.png'))# 說明測驗2
        tkimg.configure(image=bm1)
        tkimg.image = bm1
        flag_blind += 1
        r.set("flag_sound",5)
        tkimg.after(200, model_color_bindness)
    elif(flag_blind==2):
        bm1 = ImageTk.PhotoImage(Image.open(local + 'E/number.png'))
        tkimg.configure(image=bm1)
        tkimg.image = bm1
        if(int(r.get("flag_sound"))!=5):
            flag_blind += 1
        tkimg.after(2000, model_color_bindness)

    elif(flag_blind==3):
        bm1 = ImageTk.PhotoImage(Image.open(local + 'E/色盲2.png'))# 測驗圖片
        tkimg.configure(image=bm1)
        tkimg.image = bm1
        flag_blind += 1
        tkimg.after(1500, model_color_bindness)
    elif (flag_blind == 4):
        bm1 = ImageTk.PhotoImage(Image.open(local + 'E/色盲2.png'))# 測驗圖片
        tkimg.configure(image=bm1)
        tkimg.image = bm1
        gesture = str(r.get('gesture'))
        print(gesture)
        if(gesture=="up" or gesture=="cycle"):
            gesture_reco=gesture_co_1[gesture]
            print(gesture_reco)
            doc['blind'] = str(gesture_reco)# 載入測驗結果
            flag_blind += 1
        tkimg.after(150, model_color_bindness)
    elif (flag_blind == 5):
        bm1 = ImageTk.PhotoImage(Image.open(local + 'E/色盲3.jpg'))# 測驗圖片
        tkimg.configure(image=bm1)
        tkimg.image = bm1
        flag_blind += 1
        tkimg.after(1500, model_color_bindness)
    elif (flag_blind == 6):
        bm1 = ImageTk.PhotoImage(Image.open(local + 'E/色盲3.jpg'))# 測驗圖片
        tkimg.configure(image=bm1)
        tkimg.image = bm1
        gesture = str(r.get('gesture'))
        print(gesture)
        if(gesture=="up" or gesture=="cycle"): # 接收手勢
            gesture_reco=gesture_co_1[gesture]
            print(gesture_reco)
            doc['blind-1'] = str(gesture_reco)# 載入測驗結果
            flag_blind += 1
        tkimg.after(200, model_color_bindness)
    elif (flag_blind == 7):
        bm1 = ImageTk.PhotoImage(Image.open(local + 'E/通通遮起來.png'))
        tkimg.configure(image=bm1)
        tkimg.image = bm1
        flag_blind += 1
        tkimg.after(200, model_yello_problem) # 跳至下一測驗



# mosqutio 
flag_mosqito=0
def model_mosqito():
    global flag_mosqito
    if(flag_mosqito==0):
        bm1 = ImageTk.PhotoImage(Image.open(local+'E/mostito.png'))# 說明測驗
        tkimg.configure(image=bm1)
        tkimg.image = bm1
        flag_mosqito+=1
        tkimg.after(2000, model_mosqito)
    elif(flag_mosqito==1):
        bm1 = ImageTk.PhotoImage(Image.open(local + 'E/mostito1.jpg'))# 說明測驗
        tkimg.configure(image=bm1)
        tkimg.image = bm1
        flag_mosqito+=1
        r.set("flag_sound",6)
        tkimg.after(200, model_mosqito)
    elif(flag_mosqito==2):
        bm1 = ImageTk.PhotoImage(Image.open(local + 'E/mostito1.jpg'))# 說明測驗
        tkimg.configure(image=bm1)
        tkimg.image = bm1
        if(int(r.get("flag_sound"))!=6):
            flag_mosqito+=1
        tkimg.after(2000, model_mosqito)
    elif(flag_mosqito==3):
        bm1 = ImageTk.PhotoImage(Image.open(local + 'E/通通遮起來.png'))# 測驗圖片
        tkimg.configure(image=bm1)
        tkimg.image = bm1
        flag_mosqito += 1
        tkimg.after(1000, model_mosqito)
    elif(flag_mosqito==4):
        bm1 = ImageTk.PhotoImage(Image.open(local + 'E/通通遮起來.png'))# 測驗圖片
        tkimg.configure(image=bm1)
        tkimg.image = bm1
        gesture = str(r.get('gesture'))
        print(gesture)
        if(gesture=="up" or gesture=="cycle"):
            gesture_reco=gesture_co_2[gesture]
            print(gesture_reco)
            doc['mosqito'] = str(gesture_reco)# 載入測驗結果
            tkimg.after(200, model_score)
        tkimg.after(200, model_mosqito)

# yellow problem
flag_yellow=0
def model_yello_problem():
    global flag_yellow
    if(flag_yellow==0):
        bm1 = ImageTk.PhotoImage(Image.open(local+'E/yellow.png'))# 說明測驗
        tkimg.configure(image=bm1)
        tkimg.image = bm1
        flag_yellow+=1
        tkimg.after(2000, model_yello_problem)
    elif(flag_yellow==1):
        bm1 = ImageTk.PhotoImage(Image.open(local + 'E/yellow_chart.png'))# 說明測驗
        tkimg.configure(image=bm1)
        tkimg.image = bm1
        flag_yellow+=1
        r.set("flag_sound",7)
        tkimg.after(200, model_yello_problem)
    elif(flag_yellow==2):
        bm1 = ImageTk.PhotoImage(Image.open(local + 'E/yellow_chart.png'))
        tkimg.configure(image=bm1)
        tkimg.image = bm1
        if(int(r.get("flag_sound"))!=7):
            flag_yellow+=1
        tkimg.after(2000, model_yello_problem)
    elif(flag_yellow==3):
        bm1 = ImageTk.PhotoImage(Image.open(local + 'E/yellow_test.jpg'))# 測驗圖片
        tkimg.configure(image=bm1)
        tkimg.image = bm1
        flag_yellow+=1
        tkimg.after(1500, model_yello_problem)
    elif (flag_yellow == 4):
        bm1 = ImageTk.PhotoImage(Image.open(local + 'E/yellow_test.jpg'))# 測驗圖片
        tkimg.configure(image=bm1)
        tkimg.image = bm1
        print('input ....')
        gesture = str(r.get('gesture'))
        print(gesture)
        if(gesture=="up" or gesture=="cycle"):
            gesture_reco=gesture_co_2[gesture]
            print(gesture_reco)
            doc['yellow'] = str(gesture_reco)# 載入測驗結果
            flag_yellow += 1
        tkimg.after(200, model_yello_problem)
    elif (flag_yellow == 5):
        bm1 = ImageTk.PhotoImage(Image.open(local + 'E/通通遮起來.png'))
        tkimg.configure(image=bm1)
        tkimg.image = bm1
        flag_yellow += 1
        tkimg.after(200, model_mosqito)


# save the test result to firebase 
def save():
    d=time.strftime("%Y-%m-%d", time.localtime()) 
    right=doc["right_show"][0:1]
    left=doc["left_show"][0:1]
    user_info.update({u'blind': doc["blind"]})
    user_info.update({u'eye_left': left})
    user_info.update({u'eye_right': right})
    user_info.update({u'eye_flash_left': doc["flash_left"]})
    user_info.update({u'eye_flash_right': doc["flash_right"]})
    user_info.update({u'mostiquto': doc["mosqito"]})
    user_info.update({u'yellow': doc["yellow"]})
    user_info.update({u'date': str(d)})
    user_info.update({u'eye_left_real': doc["left"]})
    user_info.update({u'eye_right_real': doc["right"]})

    #eye_tem= db.collection(u'User').document(u''+email)
    #eye_temp=eye_tem.get().to_dict()["eye_temp"]
   	#print(eye_temp)

# 判斷視力範圍
def calculate(score):
    text="non"
    if(0.1<=score <=0.3):
        text=coor_score["0.1-0.3"]
    elif(0.4<=score<=0.7 ):
        text=coor_score["0.4-0.7"]
    elif(0.8<=score <=1.1  ):
        text=coor_score["0.8-1.1"]
    elif(1.2<=score<=1.5 ):
        text=coor_score["1.2-1.5"]
    elif(1.5<=score<=2.0 ):
        text=coor_score["1.5-2.0"]   
    return text

# 對應視力的好壞程度
def calculate_recom(left,right,flash_right,flash_left,blind,blind_1,mosqutio,yellow):
    text=""
    if(flash_right=="有"or flash_left=="有"or blind=="有"or blind_1=="有"or mosqutio=="有"or yellow=="有" or left=="Worst" or left=="Bad" or right=="Worst" or right=="Bad" ):
        text=coor_recom["Worst"]
        doc["color"]="red"
    elif(left=="Good" or right=="Good"):
        text=coor_recom["Good"]
        doc["color"]="black"
    elif(left=="Nice" or right=="Nice"):
        text=coor_recom["Nice"]
        doc["color"]="black"
    elif(left=="Excellent" or right=="Excellent"):
        text=coor_recom["Excellent"]
        doc["color"]="black" 
    return text  

   



#show the all result in the screen 
def model_score():
    tkimg.configure(image="")
    # all result variable 
    text_left=float(doc["left"])
    text_right=float(doc["right"])
    flash_left=doc["flash_left"]
    flash_right=doc["flash_right"]
    blind=doc['blind']
    blind_1=doc['blind-1']
    mosqutio=doc['mosqito']
    yellow=doc["yellow"]
    right=calculate(text_right)
    left=calculate(text_left)
    doc["right_show"]=right
    doc["left_show"]=left
    healthy_state=calculate_recom(left,right,flash_right,flash_left,blind,blind_1,mosqutio,yellow)

    # show resulte on tkinter 
    left_eye= Label(root,text="左眼視力 :  "+left,font=("Calibri",40),bg="white")
    right_eye = Label(root, text="右眼視力 :  "+right,font=("Calibri",40),bg="white")
    left_flash = Label(root, text="左眼散光 :  "+flash_left,font=("Calibri",40),bg="white")
    right_flash = Label(root, text="右眼散光 :  "+flash_right,font=("Calibri",40),bg="white")
    color_bindness = Label(root, text="色盲 :  "+blind+" / "+blind_1,font=("Calibri",40),bg="white")
    mosqito = Label(root, text="飛蚊症 :  "+mosqutio,font=("Calibri",40),bg="white")
    yello_problem = Label(root, text="黃斑部病變 :  "+yellow,font=("Calibri",40),bg="white")
    state = Label(root, text="健康狀況 :  "+healthy_state,font=("Calibri",40),bg="white",fg=doc["color"])
    #the text location 
    left_eye.place(relx=.25, rely=.1)
    right_eye.place(relx=.55, rely=.1)
    left_flash.place(relx=.25, rely=.29)
    right_flash.place(relx=.55, rely=.29)
    color_bindness.place(relx=.25, rely=.48)
    mosqito.place(relx=.25, rely=.67)
    yello_problem.place(relx=.55, rely=.48)
    state.place(relx=.25, rely=.85)
    save()
    r.set("flag_sound",-1) # close the sound 
    tkimg.after(13000, cancel) # stop the process 


def cancel():
    root.destroy() # close the system 


#tkimg.after(1500, model_flash)
#tkimg.after(1500, model_distance_0)
root.mainloop()


