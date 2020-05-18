from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from tracker.models import User

class AuthBackend(BaseBackend):

    def authenticate(self, request, username=None, password=None):
        user = User.objects.get(username=username)
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None