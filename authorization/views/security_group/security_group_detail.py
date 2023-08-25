from django.views.generic import DetailView
from django.core.paginator import Paginator

from authorization.models import AccessPermission, Permission, SecurityGroup

from django.contrib.auth.mixins import LoginRequiredMixin
from organisation.models import Profile
from openea.utils import Utils

class SecurityGroupDetailView(LoginRequiredMixin, DetailView):
    model = SecurityGroup
    template_name = "security_group/security_group_detail.html"
    paginate_by = 10000
    permission_required = [(Utils.PERMISSION_ACTION_VIEW, model.get_object_type(), None)]

    def get_context_data(self, **kwargs):
        context = super(SecurityGroupDetailView, self).get_context_data(**kwargs)
        context['organisation_id'] = self.object.organisation.id

        accesspermission_list = AccessPermission.objects.filter(security_group_accesspermissions__in=[self.object]).order_by('permission__object_type').order_by('permission__action').all()
        accesspermission_paginator = Paginator(accesspermission_list, self.paginate_by)
        accesspermission_page_number = self.request.GET.get('accesspermission_page')
        context['accesspermissions'] = accesspermission_paginator.get_page(accesspermission_page_number)

        profile_list = Profile.objects.filter(security_groups__in=[self.object]).order_by('-created_at').all()
        profile_paginator = Paginator(profile_list, self.paginate_by)
        profile_page_number = self.request.GET.get('profile_page')
        context['profiles'] = profile_paginator.get_page(profile_page_number)
        
        return context

