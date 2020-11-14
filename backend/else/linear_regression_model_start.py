import redis
r1 = redis.Redis(host='140.136.155.36', port=6379,password='123456')
r1.set("ana_flag",'open')