from django.contrib.auth.models import User
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
import jwt

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if auth_header and auth_header.startswith('Bearer '):
            try:
                token = request.COOKIES.get('jwt_token')
                decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                username = decoded_token['username']
                user = User.objects.get(username=username)
                return (user, None)
            except (jwt.exceptions.DecodeError, User.DoesNotExist):
                pass

        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
    def bypass_authentication(self, request):

        bypass_urls = [
            'user/register/',
            'user/signin/signout',
        ]

        for url in bypass_urls:
            if request.path_info.startswith(url):
                return True

        return False
