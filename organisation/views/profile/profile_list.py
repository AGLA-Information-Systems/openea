from django.views.generic import ListView

from django.contrib.auth.mixins import LoginRequiredMixin
from openea.utils import Utils
from utils.views.custom import MultipleObjectsView


from organisation.models import Profile
from openea.utils import Utils

class ProfileListView(LoginRequiredMixin, MultipleObjectsView, ListView):
    model = Profile
    template_name = "profile/profile_list.html"
    paginate_by = 10000
    permission_required = [(Utils.PERMISSION_ACTION_LIST, model.get_object_type(), None)]


class ProfileListUserView(LoginRequiredMixin, MultipleObjectsView, ListView):
    model = Profile
    template_name = "profile/profile_list.html"
    paginate_by = 10000
    permission_required = [(Utils.PERMISSION_ACTION_LIST, model.get_object_type(), None)]

    def get_queryset(self):
        # search = self.request.GET.get('search')
        # if search:
        #     qs = qs.filter(advertiser__name__icontains=search)
        # qs = qs.order_by("-id") # you don't need this if you set up your ordering on the model
        qs = super().get_queryset() 
        return qs.filter(user=self.request.user)


class ProfileListOrganisationView(LoginRequiredMixin, MultipleObjectsView, ListView):
    model = Profile
    template_name = "profile/profile_list.html"
    paginate_by = 10000
    permission_required = [(Utils.PERMISSION_ACTION_LIST, model.get_object_type(), None)]

    def get_queryset(self):
        qs = super().get_queryset() 
        return qs.filter(organisation__id=self.kwargs['organisation_id'])