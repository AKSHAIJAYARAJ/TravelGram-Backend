import os,sys
import django
import re
from .models import UserModel
from .serializers import UserActionManagerSerializer
from database_manager.redis_executer import RedisManager
import bcrypt

sys.path.append("/opt/projects-A/trip_media/")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trip_media.settings')
# django.setup()

class User:
    def __init__(self):
        self.user_serializer = UserActionManagerSerializer
    # def is_exist(self):
    #     pass
    def register(self,data : dict):

        validator = self.user_serializer(data=data)
        if validator.is_valid():
            try :
                if 'user_phone_number' in data.keys():
                    if re.match(r'(\+[0-9]+\s*)?(\([0-9]+\))?[\s0-9\-]+[0-9]+', data['user_phone_number']):
                        username = data['user_phone_number']
                elif 'user_email' in data.keys():
                    if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', data['user_email']):
                        username = data['user_email']
                if not username:
                    return {"status":"error","result":"",'message':'Invalid Phone numner or Email id'}
                existing_users = RedisManager().get(key= 'registerd-users')
                if not existing_users:
                    RedisManager().upsert(value=[username],key='registerd-users')
                elif existing_users and username not in existing_users:
                    RedisManager().append(value=[username],key='registerd-users')
                else:
                    return {"status":"error","result":"",'message':'Username already exists'}
                salt = bcrypt.gensalt()
                hashed_password = bcrypt.hashpw(data['user_pass_word'].encode('utf-8'), salt)
                validator.validated_data['user_pass_word'] = hashed_password
                validator.save()
                return {"status":"ok","result":"",'message':'User Created'}
            except Exception as e:
                print('-----USER EPTN-----',e)
                return {"status":"error","result":"",'message':'error'}
        else:
            return {"status":"error","result":"",'message':'Invalid data'}

    def log_in(self, data : dict):
        validator = self.user_serializer(data=data)
        if validator.is_valid():
            try:
                username = data['user_phone_number'] if 'user_phone_number' in data.keys() else data['user_email']
                existing_users = RedisManager().get(key= 'registerd-users')
                if username in existing_users:
                    RedisManager().append(value=[username],key='registerd-users')
                else:
                    return {"status":"error","result":"",'message':'Username already exists'}
                
            except:
                pass
        else:
            return {"status":"error","result":"",'message':'Invalid data'}

    def log_out(self):
        pass
    def reset_password(self):
        pass