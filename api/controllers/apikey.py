from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import authentication

from api.models import APIKey

User = get_user_model()


class APIKeyAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        # Extract the JWT from the Authorization header
        api_key = request.META.get('API-KEY')
        if not api_key:
            headers = request.META.get('headers')
            if headers:
                api_key = headers.get('API-KEY')
                organisation = headers.get('organisation')
        if api_key is None:
            return None
        #TODO: source IP filtering

        # Decode the JWT and verify its signature
        try:
            key = APIKey.objects.get(key=api_key, organisation=organisation)
        except APIKey.DoesNotExist:
            return None

    def authenticate_header(self, request):
        return 'Bearer'
