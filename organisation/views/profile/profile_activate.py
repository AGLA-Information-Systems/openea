from authorization.controllers.utils import CustomPermissionRequiredMixin 
from django.contrib.auth.mixins import LoginRequiredMixin
from utils.views.custom import SingleObjectView
from organisation.models import Profile

from django.http import HttpResponseRedirect
from django.views import View
from django.urls import reverse_lazy, reverse
from django.core.exceptions import PermissionDenied
from django.db import transaction

class ProfileActivateView(LoginRequiredMixin, CustomPermissionRequiredMixin, SingleObjectView, View):
    model = Profile
    permission_required = []
    success_url = reverse_lazy('profile_list')
    initial = {}

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        profile = Profile.objects.get(id=kwargs.get('pk'))

        user_profiles = set(self.request.user.profiles.all())
        if not(profile in user_profiles):
            raise PermissionDenied()

        for user_profile in user_profiles:
            user_profile.is_active = False
            user_profile.save()
        profile.is_active = True
        profile.save()
        return HttpResponseRedirect(self.success_url)
