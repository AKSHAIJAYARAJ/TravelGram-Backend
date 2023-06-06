from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.conf import settings
import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if auth_header and auth_header.startswith('Bearer '):
            try:
                token = auth_header.split(' ')[1]
                decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])

                # Check token expiry
                expiry_timestamp = decoded_token.get('exp')
                if expiry_timestamp and datetime.utcfromtimestamp(expiry_timestamp) < datetime.utcnow():
                    raise exceptions.AuthenticationFailed('Token has expired')

                return True
            except (jwt.exceptions.DecodeError, User.DoesNotExist):
                pass

        return None

    def bypass_authentication(self, request):
        # Specify the URLs or endpoints to bypass authentication
        bypass_urls = [
            '/api/login/',
            '/api/register/',
        ]

        for url in bypass_urls:
            if request.path_info.startswith(url):
                return True

        return False
