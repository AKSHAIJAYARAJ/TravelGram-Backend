import os,sys
import django
import re
from .serializers import UserActionManagerSerializer
from database_manager.redis_executer import RedisManager
import bcrypt
from .user_crud import UserCRUD
from .models import UserModel
import datetime
import jwt
import json

with open("/opt/projects-A/trip_media/config_and_credentials/env_conf.json",'r') as conf:
    conf = json.load(conf)

sys.path.append("/opt/projects-A/trip_media/")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trip_media.settings')
django.setup()

class User:
    def __init__(self):
        self.user_serializer = UserActionManagerSerializer
    # def is_exist(self):
    #     pass
    def register(self,data : dict):

        validator = self.user_serializer(data=data)
        if validator.is_valid():
            try :
                # Username validation using regx
                if 'user_phone_number' in data.keys():
                    if re.match(r'(\+[0-9]+\s*)?(\([0-9]+\))?[\s0-9\-]+[0-9]+', data['user_phone_number']):
                        username = data['user_phone_number']
                        dgraph_payload = {"phone":username}
                elif 'user_email' in data.keys():
                    if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', data['user_email']):
                        username = data['user_email']
                        dgraph_payload = {"email":username}

                if not username:
                    return {"status":"error","result":"",'message':'Invalid Phone number or Email id'}
                
                # Check whether the user is already registered or not
                existing_users = RedisManager().get(key= 'registered-users')
                if not existing_users:
                    # Add user to registered users if user is not registered
                    RedisManager().upsert(value=[username],key='registered-users')
                elif existing_users and username not in existing_users:
                    RedisManager().append(value=[username],key='registered-users')
                else:
                    return {"status":"error","result":"",'message':'Username already exists'}
                
                # Hash the user password
                salt = bcrypt.gensalt()
                hashed_password = bcrypt.hashpw(data['user_pass_word'].encode('utf-8'), salt)
                validator.validated_data['user_pass_word'] = hashed_password
                
                # Create User in dgraph
                uuid = UserCRUD().post(user_data=dgraph_payload)

                # add uid to postgres
                validator.validated_data['user_uid'] = uuid

                # Save data to database 
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
                phone = email = ''
                if 'user_phone_number' in data.keys():
                    username = phone= data['user_phone_number'] 
                else: 
                    username = email = data['user_email']
                username = data['user_phone_number'] 
                existing_users = RedisManager().get(key= 'registered-users')
                if username in existing_users:
                    if len(phone) == 0:
                        user_data = UserModel.objects.filter(user_email = email).first()
                    else :
                        user_data = UserModel.objects.filter(user_email = phone).first()
                    if bcrypt.checkpw(data['user_password'].encode('utf-8'), user_data.user_password.encode('utf-8')):
                        payload ={
                            'id' : user_data.user_id,
                            'uuid' : user_data.user_uid,
                            'expiry' : datetime.datetime.now(),
                            'status' : True
                        }
                        token = jwt.encode(payload,key =conf['jwt_secret_key'],algorithm='HS256')
                        return {"status":"Ok","result":{'token':token},'message':'Success'}
                else:
                    return {"status":"error","result":"",'message':'user not found'}
                
            except:
                pass
        else:
            return {"status":"error","result":"",'message':'Invalid data'}

    def log_out(self):
        pass
    def reset_password(self):
        pass