from django.views.generic import ListView

from taxonomy.models import TagGroup
from django.contrib.auth.mixins import LoginRequiredMixin
from openea.utils import Utils

class TagGroupListView(LoginRequiredMixin, ListView):
    model = TagGroup
    template_name = "tag_group/tag_group_list.html"
    paginate_by = 10000
    permission_required = [(Utils.PERMISSION_ACTION_LIST, model.get_object_type(), None)]


class TagGroupListUserView(LoginRequiredMixin, ListView):
    model = TagGroup
    template_name = "tag_group/tag_group_list.html"
    paginate_by = 10000
    permission_required = [(Utils.PERMISSION_ACTION_LIST, model.get_object_type(), None)]

    def get_queryset(self):
        # search = self.request.GET.get('search')
        # if search:
        #     qs = qs.filter(advertiser__name__icontains=search)
        # qs = qs.order_by("-id") # you don't need this if you set up your ordering on the model
        qs = super().get_queryset() 
        return qs.filter(user=self.request.user)


class TagGroupListOrganisationView(LoginRequiredMixin, ListView):
    model = TagGroup
    template_name = "tag_group/tag_group_list.html"
    paginate_by = 10000
    permission_required = [(Utils.PERMISSION_ACTION_LIST, model.get_object_type(), None)]

    def get_queryset(self):
        qs = super().get_queryset() 
        return qs.filter(organisation__id=self.kwargs['organisation_id'])