from django.views.generic import DetailView
from authorization.controllers.utils import CustomPermissionRequiredMixin, create_organisation_admin_security_group
from django.contrib.auth.mixins import LoginRequiredMixin
from utils.views.custom import SingleObjectView

from organisation.models import Profile


class ProfileDetailView(LoginRequiredMixin, CustomPermissionRequiredMixin, SingleObjectView, DetailView):
    model = Profile
    template_name = "profile/profile_detail.html"
    permission_required = [('VIEW', model.get_object_type(), None)]

