
from django.contrib.auth.mixins import LoginRequiredMixin
from organisation.controllers.profile import ProfileController
from openea.utils import Utils
from utils.views.custom import SingleObjectView
from organisation.models import Profile

from django.http import HttpResponseRedirect
from django.views import View
from django.urls import reverse_lazy, reverse
from django.core.exceptions import PermissionDenied
from django.db import transaction

class ProfileActivateView(LoginRequiredMixin, SingleObjectView, View):
    model = Profile
    permission_required = []
    success_url = reverse_lazy('profile_list')
    initial = {}

    def post(self, request, *args, **kwargs):
        profile = Profile.objects.get(id=kwargs.get('pk'))
        
        ProfileController.activate(user=self.request.user, profile=profile)
        
        return HttpResponseRedirect(self.success_url)
