from django.contrib.auth.backends import BaseBackend
from .models import CustomUser
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = get_user_model().objects.get(email=username)  # Buscar por email
            if user.check_password(password):
                return user
        except get_user_model().DoesNotExist:
            return None
        