from django.views.generic import ListView

from configuration.models import Configuration
from authorization.controllers.utils import CustomPermissionRequiredMixin


class ConfigurationListView(CustomPermissionRequiredMixin, ListView):
    model = Configuration
    template_name = "configuration/configuration_list.html"
    paginate_by = 10000
    configuration_required = [('LIST', model.get_object_type(), None)]


class ConfigurationListUserView(CustomPermissionRequiredMixin, ListView):
    model = Configuration
    template_name = "configuration/configuration_list.html"
    paginate_by = 10000
    configuration_required = [('LIST', model.get_object_type(), None)]

    def get_queryset(self):
        # search = self.request.GET.get('search')
        # if search:
        #     qs = qs.filter(advertiser__name__icontains=search)
        # qs = qs.order_by("-id") # you don't need this if you set up your ordering on the model
        qs = super().get_queryset() 
        return qs.filter(user=self.request.user)


class ConfigurationListOrganisationView(CustomPermissionRequiredMixin, ListView):
    model = Configuration
    template_name = "configuration/configuration_list.html"
    paginate_by = 10000
    configuration_required = [('LIST', model.get_object_type(), None)]

    def get_queryset(self):
        qs = super().get_queryset() 
        return qs.filter(organisation__id=self.kwargs['organisation_id'])