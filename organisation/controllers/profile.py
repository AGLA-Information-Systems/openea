from django.core.exceptions import PermissionDenied
from django.db import transaction

class ProfileController:
    @staticmethod
    def activate(user, profile):
        with transaction.atomic():
            user_profiles = set(user.profiles.all())
            if not(profile in user_profiles):
                raise PermissionDenied()

            for user_profile in user_profiles:
                user_profile.is_active = False
                user_profile.save()
            profile.is_active = True
            profile.save()