from tabnanny import check
from django.views.generic import DetailView
from django.core.paginator import Paginator
from authorization.controllers.utils import CustomPermissionRequiredMixin, check_permission
from configuration.models import Configuration
from openea.utils import Utils
from taxonomy.models import Tag, TagGroup

from webapp.models import Organisation, Profile, Task
from ontology.models import Repository
from authorization.models import SecurityGroup, Permission


class OrganisationDetailView(CustomPermissionRequiredMixin, DetailView):
    model = Organisation
    template_name = "organisation/organisation_detail.html"
    paginate_by = 10000
    permission_required = [(Permission.PERMISSION_ACTION_VIEW, model.get_object_type(), None)]

    def get_context_data(self, **kwargs):
        context = super(OrganisationDetailView, self).get_context_data(**kwargs)

        context['show_repositories'] = check_permission(user=self.request.user, action=Permission.PERMISSION_ACTION_VIEW, object_type=Utils.OBJECT_REPOSITORY)
        if context['show_repositories']:
            repository_list = Repository.objects.filter(organisation=self.object).order_by('-created_at').all()
            repository_paginator = Paginator(repository_list, self.paginate_by)
            repository_page_number = self.request.GET.get('repository_page')
            context['repositories'] = repository_paginator.get_page(repository_page_number)


        context['show_profiles'] = check_permission(user=self.request.user, action=Permission.PERMISSION_ACTION_VIEW, object_type=Utils.OBJECT_PROFILE)
        if context['show_profiles']:
            profile_list = Profile.objects.filter(organisation=self.object).order_by('-created_at').all()
            profile_paginator = Paginator(profile_list, self.paginate_by)
            profile_page_number = self.request.GET.get('profile_page')
            context['profiles'] = profile_paginator.get_page(profile_page_number)


        context['show_security_groups'] = check_permission(user=self.request.user, action=Permission.PERMISSION_ACTION_VIEW, object_type=Utils.OBJECT_SECURITY_GROUP)
        if context['show_security_groups']:
            security_group_list = SecurityGroup.objects.filter(organisation=self.object).order_by('-created_at').all()
            security_group_paginator = Paginator(security_group_list, self.paginate_by)
            security_group_page_number = self.request.GET.get('security_group_page')
            context['security_groups'] = security_group_paginator.get_page(security_group_page_number)


        context['show_permissions'] = check_permission(user=self.request.user, action=Permission.PERMISSION_ACTION_VIEW, object_type=Utils.OBJECT_PERMISSION)
        if context['show_permissions']:
            permission_list = Permission.objects.filter(organisation=self.object).order_by('-created_at').all()
            permission_paginator = Paginator(permission_list, self.paginate_by)
            permission_page_number = self.request.GET.get('permission_page')
            context['permissions'] = permission_paginator.get_page(permission_page_number)


        context['show_tasks'] = check_permission(user=self.request.user, action=Permission.PERMISSION_ACTION_VIEW, object_type=Utils.OBJECT_TASK)
        if context['show_tasks']:
            task_list = Task.objects.filter(organisation=self.object).order_by('-created_at').all()
            task_paginator = Paginator(task_list, self.paginate_by)
            task_page_number = self.request.GET.get('task_page')
            context['tasks'] = task_paginator.get_page(task_page_number)

        context['show_tag_groups'] = check_permission(user=self.request.user, action=Permission.PERMISSION_ACTION_VIEW, object_type=Utils.OBJECT_TAG_GROUP)
        if context['show_tag_groups']:
            tag_group_list = TagGroup.objects.filter(organisation=self.object).order_by('-created_at').all()
            tag_group_paginator = Paginator(tag_group_list, self.paginate_by)
            tag_group_page_number = self.request.GET.get('tag_group_page')
            context['tag_groups'] = tag_group_paginator.get_page(tag_group_page_number)

        context['show_tags'] = check_permission(user=self.request.user, action=Permission.PERMISSION_ACTION_VIEW, object_type=Utils.OBJECT_TAG)
        if context['show_tags']:
            tag_list = Tag.objects.filter(tag_group__organisation=self.object).order_by('-created_at').all()
            tag_paginator = Paginator(tag_list, self.paginate_by)
            tag_page_number = self.request.GET.get('tag_page')
            context['tags'] = tag_paginator.get_page(tag_page_number)

        context['show_configurations'] = check_permission(user=self.request.user, action=Permission.PERMISSION_ACTION_VIEW, object_type=Utils.OBJECT_CONFIG)
        if context['show_configurations']:
            configuration_list = Configuration.objects.filter(organisation=self.object).order_by('-name').all()
            configuration_paginator = Paginator(configuration_list, self.paginate_by)
            configuration_page_number = self.request.GET.get('tag_page')
            context['configurations'] = configuration_paginator.get_page(configuration_page_number)    

        return context
