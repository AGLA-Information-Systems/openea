from django.views.generic import DetailView
from django.core.paginator import Paginator

from authorization.models import Permission, SecurityGroup
from authorization.controllers.utils import CustomPermissionRequiredMixin
from organisation.models import Profile


class SecurityGroupDetailView(CustomPermissionRequiredMixin, DetailView):
    model = SecurityGroup
    template_name = "security_group/security_group_detail.html"
    paginate_by = 10000
    permission_required = [('VIEW', model.get_object_type(), None)]

    def get_context_data(self, **kwargs):
        context = super(SecurityGroupDetailView, self).get_context_data(**kwargs)
        context['organisation_id'] = self.object.organisation.id

        permission_list = Permission.objects.filter(security_groups__in=[self.object]).order_by('-created_at').all()
        permission_paginator = Paginator(permission_list, self.paginate_by)
        permission_page_number = self.request.GET.get('repository_page')
        context['permissions'] = permission_paginator.get_page(permission_page_number)

        profile_list = Profile.objects.filter(security_groups__in=[self.object]).order_by('-created_at').all()
        profile_paginator = Paginator(profile_list, self.paginate_by)
        profile_page_number = self.request.GET.get('repository_page')
        context['profiles'] = profile_paginator.get_page(profile_page_number)
        
        return context

