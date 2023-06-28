# MODULE DETAILS
# __________________________________________________________________________________________________________________________
# MODULE NAME   : Authentication Middleware
# VERSION       : 1.0
# SYNOPSYS      : This module is used to authenticate requests.
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

from typing import Any
from django.conf import settings
# import jwt
from jwt.api_jws import decode
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from datetime import datetime
from database_manager.redis_executer import RedisManager
import json

class JwtAuthentication:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args: Any, **kwds: Any) -> Any:
        
        try:
            # Bypass paths which do not require authentication
            if request.path_info in settings.UNAUTH_REQUESTS:
                return self.get_response(request)
            print('---------FIRST------------')
            # Rest of the code remains unchanged
            token = request.headers.get('Authorization').split(' ')
            if self.blacklisted_token(token=token):
                response = Response(data={"status": "error", "result": "Login required", "message": "Token expired"}, status=status.HTTP_403_FORBIDDEN)
                response.accepted_renderer = JSONRenderer()
                response.accepted_media_type = "application/json"
                response.renderer_context = {}
                response.render()
                return response
            
            decoded_token = json.loads(decode(token[1], settings.SECRET_KEY, algorithms=['HS256']))
            print('---------decoded_token------------',decoded_token)
            if not decoded_token:
                response = Response(data={"status": "Error", "result": "Login required", "message": "Unauthenticated user"}, status=status.HTTP_403_FORBIDDEN)
                response.accepted_renderer = JSONRenderer()
                response.accepted_media_type = "application/json"
                response.renderer_context = {}
                response.render()
                return response
            print('---------Third------------')
            token_expiry = decoded_token["expiry"]
            now = datetime.now()
            duration = now - datetime.strptime(token_expiry, '%Y-%m-%d %H:%M:%S.%f')
            days = duration.days
            print(days)
            if days > settings.TOKEN_EXPIRY:
                response = Response(data={"status": "error", "result": "Login required", "message": "Token expired"}, status=status.HTTP_403_FORBIDDEN)
                response.accepted_renderer = JSONRenderer()
                response.accepted_media_type = "application/json"
                response.renderer_context = {}
                response.render()
                return response
           
        except Exception as e:
            print("--------Exception from middleware---------", e)
            response = Response(data={"status": "error", "result": "Login required", "message": "Unauthenticated user"}, status=status.HTTP_403_FORBIDDEN)
            response.accepted_renderer = JSONRenderer()
            response.accepted_media_type = "application/json"
            response.renderer_context = {}
            response.render()
            return response
        
        # Pass the request to the views for further processing
        return self.get_response(request)
        
    def blacklisted_token(self, token: str):

        try:
            blacklisted = RedisManager().get(key="black-listed-tokens")
            if token in blacklisted['access']:
                return 
            else: 
                return False
        except:
            return 
