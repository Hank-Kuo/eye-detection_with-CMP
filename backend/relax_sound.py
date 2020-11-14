import playsound
import redis
import os
r = redis.Redis(host='localhost', port=6379, decode_responses=True)
local=os.path.abspath('.').replace("\\","/")+"/code/" #os.path.abspath('.').replace("\\","/")+"/code/"
r.set("flag_relax",0)
# 開啟音樂
while True:
    flag=int(r.get("flag_relax"))
    if(flag==2):
        playsound.playsound(local+"sound/relax_s.mp3",True)

