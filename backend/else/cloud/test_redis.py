import redis
r = redis.Redis(host='140.136.155.36', port=6379,decode_responses=True,password='123456')
while True:
    gesture=str(r.get("gesture"))
    print(gesture=="error")
