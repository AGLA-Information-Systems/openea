from django.views.generic import ListView

from authorization.models import SecurityGroup
from authorization.controllers.utils import CustomPermissionRequiredMixin 
from django.contrib.auth.mixins import LoginRequiredMixin


class SecurityGroupListView(LoginRequiredMixin, CustomPermissionRequiredMixin, ListView):
    model = SecurityGroup
    template_name = "security_group/security_group_list.html"
    paginate_by = 10000
    permission_required = [('LIST', model.get_object_type(), None)]


class SecurityGroupListUserView(LoginRequiredMixin, CustomPermissionRequiredMixin, ListView):
    model = SecurityGroup
    template_name = "security_group/security_group_list.html"
    paginate_by = 10000
    permission_required = [('LIST', model.get_object_type(), None)]

    def get_queryset(self):
        # search = self.request.GET.get('search')
        # if search:
        #     qs = qs.filter(advertiser__name__icontains=search)
        # qs = qs.order_by("-id") # you don't need this if you set up your ordering on the model
        qs = super().get_queryset() 
        return qs.filter(user=self.request.user)


class SecurityGroupListOrganisationView(LoginRequiredMixin, CustomPermissionRequiredMixin, ListView):
    model = SecurityGroup
    template_name = "security_group/security_group_list.html"
    paginate_by = 10000
    permission_required = [('LIST', model.get_object_type(), None)]

    def get_queryset(self):
        qs = super().get_queryset() 
        return qs.filter(organisation__id=self.kwargs['organisation_id'])