from django.views.generic import ListView

from authorization.models import Permission
from authorization.controllers.utils import CustomPermissionRequiredMixin 
from django.contrib.auth.mixins import LoginRequiredMixin


class PermissionListView(LoginRequiredMixin, CustomPermissionRequiredMixin, ListView):
    model = Permission
    template_name = "permission/permission_list.html"
    paginate_by = 10000
    permission_required = [('LIST', model.get_object_type(), None)]


class PermissionListUserView(LoginRequiredMixin, CustomPermissionRequiredMixin, ListView):
    model = Permission
    template_name = "permission/permission_list.html"
    paginate_by = 10000
    permission_required = [('LIST', model.get_object_type(), None)]

    def get_queryset(self):
        # search = self.request.GET.get('search')
        # if search:
        #     qs = qs.filter(advertiser__name__icontains=search)
        # qs = qs.order_by("-id") # you don't need this if you set up your ordering on the model
        qs = super().get_queryset() 
        return qs.filter(user=self.request.user)


class PermissionListOrganisationView(LoginRequiredMixin, CustomPermissionRequiredMixin, ListView):
    model = Permission
    template_name = "permission/permission_list.html"
    paginate_by = 10000
    permission_required = [('LIST', model.get_object_type(), None)]

    def get_queryset(self):
        qs = super().get_queryset() 
        return qs.filter(organisation__id=self.kwargs['organisation_id'])