from django.views.generic import DetailView
from authorization.controllers.utils import CustomPermissionRequiredMixin

from webapp.models import Profile


class ProfileDetailView(CustomPermissionRequiredMixin, DetailView):
    model = Profile
    template_name = "profile/profile_detail.html"
    permission_required = [('VIEW', model.get_object_type(), None)]
