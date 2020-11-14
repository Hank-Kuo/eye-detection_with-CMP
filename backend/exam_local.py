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
import playsound






#需要修改的地方
local=os.path.abspath('.').replace("\\","/")+"/code/"
#os.path.abspath('.').replace("\\","/")+"/code/"




# 測驗變數
count=0
mistake=0
level=0
pic=''
k=[local+'E/0.1',local+'E/0.2',local+'E/0.4',local+'E/0.6',local+'E/0.8',local+'E/1.0',local+'E/2.0']
k1=['.png',' – 1.png',' – 2.png',' – 3.png']
flag='right'
choices = [0,1,2,3]
avg=1/4
de=0.3
de1=0.1
weights = [avg,avg,avg,avg]
gesture_co={'right':0,'down':1,'left':2,'up':3}
gesture_co_1={'up':"沒有",'cycle':"有"}
coor={"-1":"0.1","0":"0.2","1":"0.4","2":"0.6","3":"0.8","4":"1.0","5":"2.0"}

#node js with python connect 
f = open(local+"email.txt", "r")
email=f.readline()

# redis connect 
r = redis.Redis(host='localhost', port=6379, decode_responses=True)
r.set("flag_cpm",'false')


# firebase 
cred = credentials.Certificate(local+'serviceAccount.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
eye_tem= db.collection(u'User').document(u''+email)
eye_temp=eye_tem.get().to_dict()["eye_temp"]
user_info= db.collection(u'User').document(u''+email).collection(u'eyesight').document(u''+eye_temp)
doc={}




# tkinter setting 
root = Tk()
root.attributes("-fullscreen",True)
root.configure(background='white')
img = ImageTk.PhotoImage(Image.open(local+'E/teststarting.png'))
tkimg=Label(root,image = img)
tkimg.place(relx=.5, rely=.5,anchor="center")

global flag_show
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
    if(mistake!=2 and count!=3):
        #測三次
        rn = np.random.choice(choices, p=weights)
        index=choices.index(rn)
        weights=[de,de,de,de]
        weights[index]=de1
        pic=k[level]+k1[rn]
        count += 1
        bm1 = ImageTk.PhotoImage(Image.open(pic))
        tkimg.configure(image=bm1)
        tkimg.image = bm1
        print(rn)
        print(weights)
        print('pic :', pic + " mistake", mistake, ' count', count, ' level', level)
        tkimg.after(200, modelll)
    elif(count==3 and mistake!=2 and level!=6):
        #對兩個 下一個LEVEL
        level+=1
        count=0
        mistake=0
        tkimg.after(20, model)
    elif((mistake==2 or level ==6)  and flag=='right'):
        #錯兩個
        flag='left'
        print(str(level-1))
        level_1=coor[str(level-1)]
        doc['right']=level_1
        print('right eye is ',level-1)
        print('turn left eye')
        count=0
        level=0
        mistake=0
        tkimg.after(200, model_left_eye)
    elif ((mistake == 2 or level == 6)  and flag == 'left'):
        # 錯兩個
        level_1=coor[str(level-1)]
        doc['left']=level_1
        bm1 = ImageTk.PhotoImage(Image.open(local + 'E/通通遮起來.png'))
        tkimg.configure(image=bm1)
        print('left eye is ',level - 1)
        count = 0
        mistake=0
        tkimg.after(200, model_flash)
        #root.destroy()


def model_distance1():
    bm1 = ImageTk.PhotoImage(Image.open(local+'E/teststarting.png'))
    tkimg.configure(image=bm1)
    tkimg.image = bm1
    playsound.playsound(local+'sound/intial.mp3',True)
    tkimg.after(20, model_distance_2)

def model_distance():
    bm1 = ImageTk.PhotoImage(Image.open(local+'E/distancehint.png'))
    tkimg.configure(image=bm1)
    tkimg.image = bm1
    playsound.playsound(local+'sound/distance.mp3',True)
    r.set('flag_distance','true')
    while (True):
        if(float(r.get('distance'))>70):
            r.set('flag_distance','false')

            tkimg.after(20, model_right_eye_1)
            break
    

def model_distance_2():
    bm1 = ImageTk.PhotoImage(Image.open(local+'E/distancehint.png'))
    tkimg.configure(image=bm1)
    tkimg.image = bm1
    tkimg.after(20, model_distance)

def modelll():
    #Double show image
    global mistake
    global flag_mistake
    global flag_show
    global set_text
    flag_show=True
    bm1 = ImageTk.PhotoImage(Image.open(pic))
    tkimg.configure(image=bm1)
    tkimg.image = bm1
    time.sleep(1.5)
    gesture = str(r.get('gesture'))
    while(gesture=="error" or gesture == "None" or gesture=='' or gesture=="cycle"):
        gesture = str(r.get('gesture'))
        if(gesture!="error"):
            if(gesture != "None"):
                if(gesture!=""):
                    if(gesture!="cycle"):
                        break
    gesture_reco=gesture_co[gesture]
    print(gesture_reco)
    if (gesture_reco == rn):
        flag_mistake=True
        print('correct')
        set_text="E/correct.png"
    else:
        flag_mistake=False
        print('wrong')
        mistake += 1
        set_text="E/wrong.png"
    tkimg.after(20, modell1_show_mistake)



def modell1_show_mistake():
    #Double show image
    global flag_show
    global flag_mistake
    global mistake
    global set_text
# true first   false not first 
    show={"time":1000,"des":model}
    bm1 = ImageTk.PhotoImage(Image.open(local + set_text))
    tkimg.configure(image=bm1)
    tkimg.image = bm1
    if(flag_show==True):
        flag_show=False
        show["des"]=modell1_show_mistake
        show["time"]=10
    tkimg.after(show["time"], show["des"])


#右眼
def model_right_eye_1():
    bm1 = ImageTk.PhotoImage(Image.open(local+'E/coverrighteye.png'))
    tkimg.configure(image=bm1)
    tkimg.image = bm1
    tkimg.after(20, model_right_eye)

def model_right_eye():
    bm1 = ImageTk.PhotoImage(Image.open(local+'E/coverrighteye.png'))
    tkimg.configure(image=bm1)
    tkimg.image = bm1
    playsound.playsound(local+'sound/CoverRightEye.mp3',True)
    r.set('flag_cpm','true')
    tkimg.after(2000, model_empty)


def model_left_eye():
    bm1 = ImageTk.PhotoImage(Image.open(local+'E/coverlefteye.png'))
    #左眼
    tkimg.configure(image=bm1)
    tkimg.image = bm1
    tkimg.after(20, model_left_eye_1)
def model_left_eye_1():
    bm1 = ImageTk.PhotoImage(Image.open(local+'E/coverlefteye.png'))
    #左眼
    tkimg.configure(image=bm1)
    tkimg.image = bm1
    playsound.playsound(local+'sound/CoverLeftEye.mp3',True)
    tkimg.after(2000, model_empty)
def model_empty():
    #COVER EVERYTHING
    bm1 = ImageTk.PhotoImage(Image.open(local+'E/通通遮起來.png'))
    tkimg.configure(image=bm1)
    tkimg.image = bm1
    tkimg.after(20, model)



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
        tkimg.after(20, model_flash)
    elif(flag_flash==2):
        bm1 = ImageTk.PhotoImage(Image.open(local + 'E/flash_guard.png'))
        tkimg.configure(image=bm1)
        tkimg.image = bm1
        flag_flash+=1
        playsound.playsound(local+'sound/flash.mp3',True)
        tkimg.after(20, model_flash)

    elif (flag_flash == 3):
        bm1 = ImageTk.PhotoImage(Image.open(local + 'E/coverrighteye.png'))
        tkimg.configure(image=bm1)
        tkimg.image = bm1
        flag_flash += 1
        tkimg.after(20, model_flash)
    elif (flag_flash == 4):
        bm1 = ImageTk.PhotoImage(Image.open(local + 'E/coverrighteye.png'))
        tkimg.configure(image=bm1)
        tkimg.image = bm1
        flag_flash += 1
        playsound.playsound(local+'sound/CoverRightEye.mp3',True)
        tkimg.after(200, model_flash)

    elif(flag_flash == 5 or flag_flash==11):
        bm1 = ImageTk.PhotoImage(Image.open(local + 'E/flash_test.jpg'))
        tkimg.configure(image=bm1)
        tkimg.image = bm1
        flag_flash += 1
        tkimg.after(200, model_flash)
    elif(flag_flash == 6 or flag_flash==12):
        bm1 = ImageTk.PhotoImage(Image.open(local + 'E/flash_test.jpg'))
        tkimg.configure(image=bm1)
        tkimg.image = bm1
        print("input:..")
# ==6 left 
#else right 
        time.sleep(1.5)
        gesture = str(r.get('gesture'))
        print(gesture)
        while(gesture!="up" or gesture!="cycle"):
            gesture = str(r.get('gesture'))
            if(gesture=="up" or gesture=="cycle"):
                break
        gesture_reco=gesture_co_1[gesture]
        print(gesture_reco)
        if(flag_flash == 6):
            doc['flash_left'] = gesture_reco
            print('left'+gesture)
        else:
            doc['flash_right'] = gesture_reco
            print('right' + gesture)
        flag_flash += 1
        if(flag_flash==13):
            tkimg.after(200, model_color_bindness)
        tkimg.after(200, model_flash)
    elif(flag_flash==7 or flag_flash==10):
        bm1 = ImageTk.PhotoImage(Image.open(local + 'E/通通遮起來.png'))
        tkimg.configure(image=bm1)
        tkimg.image = bm1
        flag_flash+=1
        tkimg.after(20, model_flash)
    elif(flag_flash==8):
        bm1 = ImageTk.PhotoImage(Image.open(local + 'E/coverlefteye.png'))
        tkimg.configure(image=bm1)
        tkimg.image = bm1
        flag_flash += 1
        tkimg.after(20, model_flash)
    elif (flag_flash == 9):
        bm1 = ImageTk.PhotoImage(Image.open(local + 'E/coverlefteye.png'))
        tkimg.configure(image=bm1)
        tkimg.image = bm1
        flag_flash += 1
        playsound.playsound(local+'sound/CoverLeftEye.mp3',True)
        tkimg.after(20, model_flash)

#ColorBlindTest
flag_blind=0
def model_color_bindness():
    global  flag_blind
    if(flag_blind==0):
        bm1 = ImageTk.PhotoImage(Image.open(local + 'E/color_blind.png'))
        tkimg.configure(image=bm1)
        tkimg.image = bm1
        flag_blind+=1
        tkimg.after(2000, model_color_bindness)
    elif(flag_blind==1):
        bm1 = ImageTk.PhotoImage(Image.open(local + 'E/number.png'))
        tkimg.configure(image=bm1)
        tkimg.image = bm1
        flag_blind += 1
        tkimg.after(20, model_color_bindness)

    elif(flag_blind==2):
        bm1 = ImageTk.PhotoImage(Image.open(local + 'E/number.png'))
        tkimg.configure(image=bm1)
        tkimg.image = bm1
        flag_blind += 1
        playsound.playsound(local+'sound/ColorBlindTest.mp3',True)
        tkimg.after(20, model_color_bindness)


    elif(flag_blind==3):
        bm1 = ImageTk.PhotoImage(Image.open(local + 'E/色盲2.png'))
        tkimg.configure(image=bm1)
        tkimg.image = bm1
        flag_blind += 1
        tkimg.after(200, model_color_bindness)
    elif (flag_blind == 4):
        bm1 = ImageTk.PhotoImage(Image.open(local + 'E/色盲2.png'))
        tkimg.configure(image=bm1)
        tkimg.image = bm1
        time.sleep(1.5)
        gesture = str(r.get('gesture'))
        print(gesture)
        while(gesture!="up" or gesture!="cycle"):
            gesture = str(r.get('gesture'))
            if(gesture=="up" or gesture=="cycle"):
                break
        gesture_reco=gesture_co_1[gesture]
        print(gesture_reco)
        doc['blind'] = str(gesture_reco)
        flag_blind += 1
        tkimg.after(200, model_color_bindness)
    elif (flag_blind == 5):
        bm1 = ImageTk.PhotoImage(Image.open(local + 'E/色盲3.jpg'))
        tkimg.configure(image=bm1)
        tkimg.image = bm1
        flag_blind += 1
        tkimg.after(200, model_color_bindness)
    elif (flag_blind == 6):
        bm1 = ImageTk.PhotoImage(Image.open(local + 'E/色盲3.jpg'))
        tkimg.configure(image=bm1)
        tkimg.image = bm1
        time.sleep(1.5)
        gesture = str(r.get('gesture'))
        print(gesture)
        while(gesture!="up" or gesture!="cycle"):
            gesture = str(r.get('gesture'))
            if(gesture=="up" or gesture=="cycle"):
                break
        gesture_reco=gesture_co_1[gesture]
        print(gesture_reco)
        doc['blind-1'] = str(gesture_reco)
        flag_blind += 1
        tkimg.after(200, model_color_bindness)
    elif (flag_blind == 7):
        bm1 = ImageTk.PhotoImage(Image.open(local + 'E/通通遮起來.png'))
        tkimg.configure(image=bm1)
        tkimg.image = bm1
        flag_blind += 1
        tkimg.after(200, model_yello_problem)



#FlyingMosquitoTest
#        playsound.playsound(local+'sound/FlyingMosquitoTest.mp3',True)
flag_mosqito=0
def model_mosqito():
    global flag_mosqito
    if(flag_mosqito==0):
        bm1 = ImageTk.PhotoImage(Image.open(local+'E/mostito.png'))
        tkimg.configure(image=bm1)
        tkimg.image = bm1
        flag_mosqito+=1
        tkimg.after(2000, model_mosqito)
    elif(flag_mosqito==1):
        bm1 = ImageTk.PhotoImage(Image.open(local + 'E/mostito1.jpg'))
        tkimg.configure(image=bm1)
        tkimg.image = bm1
        flag_mosqito+=1
        tkimg.after(20, model_mosqito)
    elif(flag_mosqito==2):
        bm1 = ImageTk.PhotoImage(Image.open(local + 'E/mostito1.jpg'))
        tkimg.configure(image=bm1)
        tkimg.image = bm1
        flag_mosqito+=1
        playsound.playsound(local+'sound/FlyingMosquitoTest.mp3',True)
        tkimg.after(20, model_mosqito)


    elif(flag_mosqito==3):
        bm1 = ImageTk.PhotoImage(Image.open(local + 'E/通通遮起來.png'))
        tkimg.configure(image=bm1)
        tkimg.image = bm1
        flag_mosqito += 1
        tkimg.after(2000, model_mosqito)
    elif(flag_mosqito==4):
        bm1 = ImageTk.PhotoImage(Image.open(local + 'E/通通遮起來.png'))
        tkimg.configure(image=bm1)
        tkimg.image = bm1
        time.sleep(1.5)
        gesture = str(r.get('gesture'))
        print(gesture)
        while(gesture!="up" or gesture!="cycle"):
            gesture = str(r.get('gesture'))
            if(gesture=="up" or gesture=="cycle"):
                break
        gesture_reco=gesture_co_1[gesture]
        print(gesture_reco)
        doc['mosqito'] = str(gesture_reco)
        tkimg.after(200, model_score)

#yellow        playsound.playsound(local+'sound/yellow.mp3',True)
flag_yellow=0
def model_yello_problem():
    global flag_yellow
    if(flag_yellow==0):
        bm1 = ImageTk.PhotoImage(Image.open(local+'E/yellow.png'))
        tkimg.configure(image=bm1)
        tkimg.image = bm1
        flag_yellow+=1
        tkimg.after(2000, model_yello_problem)
    elif(flag_yellow==1):
        bm1 = ImageTk.PhotoImage(Image.open(local + 'E/yellow_chart.png'))
        tkimg.configure(image=bm1)
        tkimg.image = bm1
        flag_yellow+=1
        tkimg.after(20, model_yello_problem)
    elif(flag_yellow==2):
        bm1 = ImageTk.PhotoImage(Image.open(local + 'E/yellow_chart.png'))
        tkimg.configure(image=bm1)
        tkimg.image = bm1
        flag_yellow+=1
        playsound.playsound(local+'sound/yellow.mp3',True)
        tkimg.after(20, model_yello_problem)


    elif(flag_yellow==3):
        bm1 = ImageTk.PhotoImage(Image.open(local + 'E/yellow_test.jpg'))
        tkimg.configure(image=bm1)
        tkimg.image = bm1
        flag_yellow+=1
        tkimg.after(200, model_yello_problem)
    elif (flag_yellow == 4):
        bm1 = ImageTk.PhotoImage(Image.open(local + 'E/yellow_test.jpg'))
        tkimg.configure(image=bm1)
        tkimg.image = bm1
        print('input ....')
        time.sleep(1.5)
        gesture = str(r.get('gesture'))
        print(gesture)
        while(gesture!="up" or gesture!="cycle"):
            gesture = str(r.get('gesture'))
            if(gesture=="up" or gesture=="cycle"):
                break
        gesture_reco=gesture_co_1[gesture]
        print(gesture_reco)
        doc['yellow'] = str(gesture_reco)
        flag_yellow += 1
        tkimg.after(200, model_yello_problem)
    elif (flag_yellow == 5):
        bm1 = ImageTk.PhotoImage(Image.open(local + 'E/通通遮起來.png'))
        tkimg.configure(image=bm1)
        tkimg.image = bm1
        flag_yellow += 1
        tkimg.after(200, model_mosqito)
def save():
    d=time.strftime("%Y-%m-%d", time.localtime()) 
    user_info.update({u'blind': doc["blind"]})
    user_info.update({u'eye_left': doc["left"]})
    user_info.update({u'eye_right': doc["right"]})
    user_info.update({u'eye_flash_left': doc["flash_left"]})
    user_info.update({u'eye_flash_right': doc["flash_right"]})
    user_info.update({u'mostiquto': doc["mosqito"]})
    user_info.update({u'yellow': doc["yellow"]})
    user_info.update({u'date': str(d)})
    eye_tem= db.collection(u'User').document(u''+email)
    eye_temp=eye_tem.get().to_dict()["eye_temp"]
    number=(int(eye_temp[-1:])+1)%3
    print(number)
    if(number==0):
        number+=1
    eye_temp=eye_temp[0:-1]+str(number)
    eye_tem.update({u'eye_temp': eye_temp})

def model_score():
    r.set("flag_cpm",'shutdown')
    tkimg.configure(image="")
    left_eye= Label(root,text="左眼視力 :  "+doc["left"],font=("Calibri",40),bg="white")
    right_eye = Label(root, text="右眼視力 :  "+doc["right"],font=("Calibri",40),bg="white")
    left_flash = Label(root, text="左眼散光 :  "+doc["flash_left"],font=("Calibri",40),bg="white")
    right_flash = Label(root, text="右眼散光 :  "+doc["flash_right"],font=("Calibri",40),bg="white")
    color_bindness = Label(root, text="色盲 :  "+doc['blind']+" / "+doc['blind-1'],font=("Calibri",40),bg="white")
    mosqito = Label(root, text="飛蚊症 :  "+doc['mosqito'],font=("Calibri",40),bg="white")
    yello_problem = Label(root, text="黃斑部病變 :  "+doc['yellow'],font=("Calibri",40),bg="white")
    left_eye.place(relx=.25, rely=.1)
    right_eye.place(relx=.55, rely=.1)
    left_flash.place(relx=.25, rely=.29)
    right_flash.place(relx=.55, rely=.29)
    color_bindness.place(relx=.25, rely=.48)
    mosqito.place(relx=.25, rely=.67)
    yello_problem.place(relx=.25, rely=.85)
    save()
    tkimg.after(7000, cancel)



def cancel():
    root.destroy()


tkimg.after(1500,model_distance1)
root.mainloop()


