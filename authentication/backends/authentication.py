import traceback
from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.forms import ValidationError
from organisation.controllers.profile import ProfileController

User = get_user_model()


class CustomAuthenticationBackend(BaseBackend):
    """
    Authenticate
    
    """

    def authenticate(self, request, **kwargs):
        username = kwargs.get('username')
        password = kwargs.get('password')
        organisation = kwargs.get('organisation')

        if username is None or password is None:
            return None
        try:
            user = User.objects.get(Q(username=username)|Q(email=username))
            if user.is_active and user.check_password(password):
                if organisation:
                    try:
                        profile = user.profiles.get(organisation__name=organisation)
                    except Exception as e:
                        traceback.print_exc()
                        raise ValidationError("User {} is not enrolled with organisation {}".format(username, organisation))
                return user
            return None
        except User.DoesNotExist:
            return None
        

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
