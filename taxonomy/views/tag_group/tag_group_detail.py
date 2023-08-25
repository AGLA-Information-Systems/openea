from django.views.generic import DetailView
from django.core.paginator import Paginator


from django.contrib.auth.mixins import LoginRequiredMixin
from taxonomy.models import TagGroup, Tag
from openea.utils import Utils

class TagGroupDetailView(LoginRequiredMixin, DetailView):
    model = TagGroup
    template_name = "tag_group/tag_group_detail.html"
    paginate_by = 10000
    permission_required = [(Utils.PERMISSION_ACTION_VIEW, model.get_object_type(), None)]

    def get_context_data(self, **kwargs):
        context = super(TagGroupDetailView, self).get_context_data(**kwargs)
        context['organisation_id'] = self.object.organisation.id

        tag_list = Tag.objects.filter(tag_group__in=[self.object]).order_by('-created_at').all()
        tag_paginator = Paginator(tag_list, self.paginate_by)
        tag_page_number = self.request.GET.get('repository_page')
        context['tags'] = tag_paginator.get_page(tag_page_number)
        
        return context

