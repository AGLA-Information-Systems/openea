from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from openea.utils import Utils

from django.contrib.auth.mixins import LoginRequiredMixin
from organisation.models import Organisation


class OrganisationListView(LoginRequiredMixin, ListView):
    model = Organisation
    template_name = "organisation/organisation_list.html"
    paginate_by = 10000
    permission_required = [(Utils.PERMISSION_ACTION_LIST, model.get_object_type(), None)]


class OrganisationListUserView(ListView):
    model = Organisation
    template_name = "organisation/organisation_list.html"
    paginate_by = 10000
    permission_required = [(Utils.PERMISSION_ACTION_LIST, model.get_object_type(), None)]

    def get_queryset(self):
        # search = self.request.GET.get('search')
        # if search:
        #     qs = qs.filter(advertiser__name__icontains=search)
        # qs = qs.order_by("-id") # you don't need this if you set up your ordering on the model
        qs = super().get_queryset()
        organisation_ids = [x.organisation.id for x in self.request.user.profiles.all()]
        return qs.filter(id__in=organisation_ids)
