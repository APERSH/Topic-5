import redis


r = redis.Redis(host='localhost', port=6379, db=0)

def get_key(*args):
    return ":".join(map(str,args))

def get_cache(key):
    return r.get(key)

def set_cache(key, value):
    r.set(key, value)