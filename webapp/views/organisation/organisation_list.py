from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from authorization.models import Permission
from authorization.controllers.utils import CustomPermissionRequiredMixin 
from django.contrib.auth.mixins import LoginRequiredMixin
from webapp.models import Organisation


class OrganisationListView(LoginRequiredMixin, CustomPermissionRequiredMixin, ListView):
    model = Organisation
    template_name = "organisation/organisation_list.html"
    paginate_by = 10000
    permission_required = [(Permission.PERMISSION_ACTION_VIEW, model.get_object_type(), None)]


class OrganisationListUserView(ListView, CustomPermissionRequiredMixin):
    model = Organisation
    template_name = "organisation/organisation_list.html"
    paginate_by = 10000
    permission_required = [(Permission.PERMISSION_ACTION_VIEW, model.get_object_type(), None)]

    def get_queryset(self):
        # search = self.request.GET.get('search')
        # if search:
        #     qs = qs.filter(advertiser__name__icontains=search)
        # qs = qs.order_by("-id") # you don't need this if you set up your ordering on the model
        qs = super().get_queryset() 
        return qs.filter(user=self.request.user)
