# MODULE DETAILS
# __________________________________________________________________________________________________________________________
# MODULE NAME   : RedisManager
# VERSION       : 1.0
# SYNOPSYS      : This module is developed to perform redis operations.
# AUTHOR        : AKSHAI JAYARAJ
# CREATED ON    : 2023-MAY-27
# METHODS       : 
# 
# ENHANCEMENT HISTORY
# __________________________________________________________________________________________________________________________
# AUTHOR        : <AUTHOR>
# CREATED ON    : <CREATED ON>
# METHODS       : <METHODS>
# __________________________________________________________________________________________________________________________
import sys
sys.path.append("/opt/projects-A/trip_media/")
from redis import Redis
import json 
with open("/opt/projects-A/trip_media/config_and_credentials/env_conf.json",'r') as conf:
    redis_conf = json.load(conf)

class RedisManager:

    def __init__(self):
        self.redis_client = Redis(
            port=redis_conf['redis']['port'],
            # password='',
            host=redis_conf['redis']['host'],
            # username=redis_conf['redis']['user-name']
            )
        
    def upsert(self,value ,key :str):
        try:
            value = json.dumps(value)
            self.redis_client.set(key,value)
            return True
        except:
           return False 
    
    def get(self,key : str):
        try:
            return json.loads(self.redis_client.get(key))
        except:
           return False 

    def delete(self,key : str):
        try:
            self.redis_client.delete(key)
            return True
        except:
           return False 
    def append(self,value ,key :str):
        try:
            current_data  = self.get(key=key)

            if isinstance(current_data,list) and isinstance(value,list):
                
                current_data.extend(value)

            elif isinstance(current_data,dict) and isinstance(value,dict):

                current_data.update(value)
            else:
                raise TypeError("Cannont concat diffrent data types")
            self.upsert(value=current_data,key=key)
            return True
        except:
           return False 

# data = RedisManager().get(key='registerd-users')
# print(data)
# RedisManager().delete(key='registerd-users')