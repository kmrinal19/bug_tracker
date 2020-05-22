from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from tracker.models import User

class AuthBackend(BaseBackend):
    '''
    This authentication backends logs in user without the use of password
    '''

    def authenticate(self, request, userId=None, password=None):
        user = User.objects.get(userId=userId)
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None