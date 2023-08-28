from tabnanny import check
from django.conf import settings
from django.views.generic import DetailView
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from configuration.models import Configuration
from openea.utils import Utils
from taxonomy.models import Tag, TagGroup
from openea.utils import Utils
from utils.views.custom import SingleObjectView

from organisation.models import Organisation, Profile, Task
from ontology.models import Repository
from authorization.models import AccessPermission, SecurityGroup, Permission


class OrganisationDetailView(LoginRequiredMixin, SingleObjectView, DetailView):
    model = Organisation
    template_name = "organisation/organisation_detail.html"
    paginate_by = 10000
    permission_required = [(Utils.PERMISSION_ACTION_VIEW, model.get_object_type(), None)]

    def get_context_data(self, **kwargs):
        context = super(OrganisationDetailView, self).get_context_data(**kwargs)
            
        context['show_repositories'] = self.request.user.acl.check(organisation=self.organisation, permissions_required=(Utils.PERMISSION_ACTION_VIEW, Repository.get_object_type(), None))
        if context['show_repositories']:
            object_list_qs = Repository.objects.filter(organisation=self.object)
            repository_list = self.get_object_list_qs(object_list_qs=object_list_qs).order_by('name').all()
            repository_paginator = Paginator(repository_list, self.paginate_by)
            repository_page_number = self.request.GET.get('repository_page')
            context['repositories'] = repository_paginator.get_page(repository_page_number)


        context['show_profiles'] = self.request.user.acl.check(organisation=self.organisation, permissions_required=(Utils.PERMISSION_ACTION_VIEW, Profile.get_object_type(), None))
        if context['show_profiles']:
            object_list_qs = Profile.objects.filter(organisation=self.object)
            profile_list = self.get_object_list_qs(object_list_qs=object_list_qs).order_by('-created_at').all()
            profile_paginator = Paginator(profile_list, self.paginate_by)
            profile_page_number = self.request.GET.get('profile_page')
            context['profiles'] = profile_paginator.get_page(profile_page_number)


        context['show_security_groups'] = self.request.user.acl.check(organisation=self.organisation, permissions_required=(Utils.PERMISSION_ACTION_VIEW, SecurityGroup.get_object_type(), None))
        if context['show_security_groups']:
            object_list_qs = SecurityGroup.objects.filter(organisation=self.object)
            security_group_list = self.get_object_list_qs(object_list_qs=object_list_qs).order_by('-created_at').all()
            security_group_paginator = Paginator(security_group_list, self.paginate_by)
            security_group_page_number = self.request.GET.get('security_group_page')
            context['security_groups'] = security_group_paginator.get_page(security_group_page_number)


        context['show_accesspermissions'] = self.request.user.acl.check(organisation=self.organisation, permissions_required=(Utils.PERMISSION_ACTION_VIEW, AccessPermission.get_object_type(), None))
        if context['show_accesspermissions']:
            object_list_qs = AccessPermission.objects.filter(organisation=self.object)
            accesspermission_list = self.get_object_list_qs(object_list_qs=object_list_qs).order_by('permission__object_type').order_by('permission__action').all()
            accesspermission_paginator = Paginator(accesspermission_list, self.paginate_by)
            accesspermission_page_number = self.request.GET.get('accesspermission_page')
            context['accesspermissions'] = accesspermission_paginator.get_page(accesspermission_page_number)


        context['show_tasks'] = self.request.user.acl.check(organisation=self.organisation, permissions_required=(Utils.PERMISSION_ACTION_VIEW, Task.get_object_type(), None))
        if context['show_tasks']:
            object_list_qs = Task.objects.filter(organisation=self.object)
            task_list = self.get_object_list_qs(object_list_qs=object_list_qs).order_by('-created_at').all()
            task_paginator = Paginator(task_list, self.paginate_by)
            task_page_number = self.request.GET.get('task_page')
            context['tasks'] = task_paginator.get_page(task_page_number)

        context['show_tag_groups'] = self.request.user.acl.check(organisation=self.organisation, permissions_required=(Utils.PERMISSION_ACTION_VIEW, TagGroup.get_object_type(), None))
        if context['show_tag_groups']:
            object_list_qs = TagGroup.objects.filter(organisation=self.object)
            tag_group_list = self.get_object_list_qs(object_list_qs=object_list_qs).order_by('name').all()
            tag_group_paginator = Paginator(tag_group_list, self.paginate_by)
            tag_group_page_number = self.request.GET.get('tag_group_page')
            context['tag_groups'] = tag_group_paginator.get_page(tag_group_page_number)

        context['show_tags'] = self.request.user.acl.check(organisation=self.organisation, permissions_required=(Utils.PERMISSION_ACTION_VIEW, Tag.get_object_type(), None))
        if context['show_tags']:
            object_list_qs = Tag.objects.filter(tag_group__in=tag_group_list)
            tag_list = object_list_qs.order_by('name').all()
            tag_paginator = Paginator(tag_list, self.paginate_by)
            tag_page_number = self.request.GET.get('tag_page')
            context['tags'] = tag_paginator.get_page(tag_page_number)

        context['show_configurations'] = self.request.user.acl.check(organisation=self.organisation, permissions_required=(Utils.PERMISSION_ACTION_VIEW, Configuration.get_object_type(), None))
        if context['show_configurations']:
            object_list_qs = Configuration.objects.filter(organisation=self.object)
            configuration_list = self.get_object_list_qs(object_list_qs=object_list_qs).order_by('name').all()
            configuration_paginator = Paginator(configuration_list, self.paginate_by)
            configuration_page_number = self.request.GET.get('tag_page')
            context['configurations'] = configuration_paginator.get_page(configuration_page_number)    

        return context

    def get_object_list_qs(self, object_list_qs):
        if self.request.user.is_staff:
            return object_list_qs
        if self.request.user.active_profile is not None:
            return object_list_qs.filter(organisation=self.request.user.active_profile.organisation)
        return object_list_qs.none()
