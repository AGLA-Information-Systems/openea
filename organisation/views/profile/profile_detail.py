from django.views.generic import DetailView
from authorization.controllers.utils import CustomPermissionRequiredMixin
from utils.views.custom import SingleObjectView

from organisation.models import Profile


class ProfileDetailView(CustomPermissionRequiredMixin, SingleObjectView, DetailView):
    model = Profile
    template_name = "profile/profile_detail.html"
    permission_required = [('VIEW', model.get_object_type(), None)]
