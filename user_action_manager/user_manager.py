# MODULE DETAILS
# __________________________________________________________________________________________________________________________
# MODULE NAME   : Authentication Middleware
# VERSION       : 1.0
# SYNOPSYS      : This module handles user action such as login/logout, register and reset password.
# AUTHOR        : AKSHAI JAYARAJ
# CREATED ON    : 2023-JUNE-11
# METHODS       : 
# 
# ENHANCEMENT HISTORY
# __________________________________________________________________________________________________________________________
# AUTHOR        : <AUTHOR>
# CREATED ON    : <CREATED ON>
# METHODS       : <METHODS>
# __________________________________________________________________________________________________________________________
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
from django.conf import settings

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
                hashed_password = bcrypt.hashpw(data['user_password'].encode('utf-8'), salt)
                validator.validated_data['user_password'] = hashed_password.decode('utf-8')
                
                # Create User in dgraph
                uuid = UserCRUD().post(user_data=dgraph_payload)

                # add uid to postgres
                validator.validated_data['user_uid'] = uuid

                print("validator",validator.validated_data)

                # Save data to database 
                validator.save()

                return {"status":"ok","result":"",'message':'User Created'}
            except Exception as e:
                print('-----USER EPTN-----',e)
                return {"status":"error","result":"",'message':'error'}
        else:
            return {"status":"error","result":"",'message':'Invalid data'}

    def log_in(self, data : dict):
        print('---------log_in------------',data)
        # Validate the request body
        validator = self.user_serializer(data=data)
        # if valid
        if validator.is_valid():
            try:
                # Check whether the user exists, if not return user do not exists.
                phone = email = ''
                if 'user_phone_number' in data.keys():
                    username = phone= data['user_phone_number'] 
                else: 
                    username = email = data['user_email']
                # username = data['user_phone_number'] 
                print("-------USER NAME---------",phone)
                existing_users = RedisManager().get(key= 'registered-users')
                # if User exists, Check the credentials are correct.
                if username in existing_users:
                    if len(phone) == 0:
                        print('------IF-----')
                        user_data = UserModel.objects.filter(user_email = email).first()
                    else :
                        print('------ELSE-----')
                        user_data = UserModel.objects.filter(user_phone_number = phone).first()
                    print("-------USER DATA---------",user_data)
                    if bcrypt.checkpw(data['user_password'].encode('utf-8'), user_data.user_password.encode('utf-8')):
                        payload ={
                            'id' : user_data.user_id,
                            'uuid' : user_data.user_uid,
                            'expiry' : str(datetime.datetime.now()),
                            'status' : True
                        }
                        # Generate and return token
                        token = jwt.encode(payload,key =settings.SECRET_KEY,algorithm='HS256')
                        #TODO store token in redis
                        print("------",token)
                        return {"status":"Ok","result":{'token':token},'message':'Success'}
                else:
                    return {"status":"error","result":"",'message':'user not found'}
                
            except Exception as e:
                print(e)
                pass
        else:
            return {"status":"error","result":"",'message':'Invalid data'}

    def log_out(self,token: str):
        # Get blacklisted tokens
        black_listed= RedisManager().get(key= 'black-listed-tokens')
        # Add current token to blacklisted token.
        if black_listed:
            if black_listed['access']:
                black_listed['access'].append(token)
                RedisManager().upsert(value=black_listed,key='black-listed-tokens')
            else:
                black_listed ={'access':[token]}
                RedisManager().append(value=black_listed,key='black-listed-tokens')
        else:
            black_listed ={'access':[token]}
            RedisManager().upsert(value=black_listed,key='black-listed-tokens')
        # Return response
        return {"status":"ok","result":"",'message':'Successfully signed out'}
    def reset_password(self):
        pass