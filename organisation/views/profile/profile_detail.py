from django.views.generic import DetailView

from django.contrib.auth.mixins import LoginRequiredMixin
from openea.utils import Utils

from utils.views.custom import SingleObjectView

from organisation.models import Profile
from openea.utils import Utils

class ProfileDetailView(LoginRequiredMixin, SingleObjectView, DetailView):
    model = Profile
    template_name = "profile/profile_detail.html"
    permission_required = [(Utils.PERMISSION_ACTION_VIEW, model.get_object_type(), None)]
