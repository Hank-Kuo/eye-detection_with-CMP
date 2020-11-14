import playsound
import redis
import os
r = redis.Redis(host='localhost', port=6379, decode_responses=True)
r1 = redis.Redis(host='140.136.155.36', port=6379, decode_responses=True,password='123456')
r.set("flag_sound",0)
local= os.path.abspath('.').replace("\\","/")+"/code/"
#os.path.abspath('.').replace("\\","/")+"/code/"


# 聲音控制
while True:
	gesture=str(r1.get("gesture"))
	r.set("gesture",gesture)
	gesture_flag=str(r1.get("gesture_flag"))
	r.set("gesture_flag",gesture_flag)
	flag=int(r.get("flag_sound"))
	if(flag==1):
		playsound.playsound(local+"sound/distance.mp3",True)
		r.set('flag_sound',0)
	elif(flag==2):
		playsound.playsound(local+"sound/CoverLeftEye.mp3",True)
		r.set('flag_sound',0)
	elif(flag==3):
		playsound.playsound(local+"sound/CoverRightEye.mp3",True)
		r.set('flag_sound',0)
	elif(flag==4):
		playsound.playsound(local+"sound/flash.mp3",True)
		r.set('flag_sound',0)
	elif(flag==5):
		playsound.playsound(local+"sound/ColorBlindTest.mp3",True)
		r.set('flag_sound',0)
	elif(flag==6):
		playsound.playsound(local+"sound/FlyingMosquitoTest.mp3",True)
		r.set('flag_sound',0)
	elif(flag==7):
		playsound.playsound(local+"sound/yellow.mp3",True)
		r.set('flag_sound',0)
	
	elif(flag==8):
		playsound.playsound(local+"sound/ColorBlindTest.mp3",True)
		r.set('flag_sound',0)
	elif(flag==9):
		playsound.playsound(local+"sound/description.mp3",True)
		r.set('flag_sound',0)
	elif(flag==10):
		playsound.playsound(local+"sound/CoverRightEye.mp3",True)
		r.set('flag_sound',0)
	elif(flag==11):
		playsound.playsound(local+"sound/CoverLeftEye.mp3",True)
		r.set('flag_sound',0)
	elif(flag==12):
		playsound.playsound(local+"sound/intial.mp3",True)
		r.set('flag_sound',0)
	elif(flag==-1):
		r.set('flag_sound',0)
		break


