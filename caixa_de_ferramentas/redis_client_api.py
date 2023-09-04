import redis
import json

class RedisAPI:

    def __init__(self, host, port):
        self.redis = redis.Redis(host=host, port=port, decode_responses=True)
     
     
    def insert_key(self, key, value, overwrite=True) -> None :
        key_exists = self.redis.exists(key)
        if (key_exists and overwrite) or not key_exists :
            self.redis.set(key, json.dumps(value))
        else:
            print(f'Key {key} already exists')


    def get_key(self, key, default=[]):
        data = self.redis.get(key)
        if data is None:
            return default
        return json.loads(data)
    
    
    def delete_key(self, key):
        self.redis.delete(key)


    def clear_keys(self):
        self.redis.flushall()


    def list_keys(self):
        return self.redis.keys()
   

    
        