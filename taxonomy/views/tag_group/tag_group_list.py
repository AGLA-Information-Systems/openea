from django.views.generic import ListView

from taxonomy.models import TagGroup
from authorization.controllers.utils import CustomPermissionRequiredMixin 
from django.contrib.auth.mixins import LoginRequiredMixin


class TagGroupListView(LoginRequiredMixin, CustomPermissionRequiredMixin, ListView):
    model = TagGroup
    template_name = "tag_group/tag_group_list.html"
    paginate_by = 10000
    permission_required = [('LIST', model.get_object_type(), None)]


class TagGroupListUserView(LoginRequiredMixin, CustomPermissionRequiredMixin, ListView):
    model = TagGroup
    template_name = "tag_group/tag_group_list.html"
    paginate_by = 10000
    permission_required = [('LIST', model.get_object_type(), None)]

    def get_queryset(self):
        # search = self.request.GET.get('search')
        # if search:
        #     qs = qs.filter(advertiser__name__icontains=search)
        # qs = qs.order_by("-id") # you don't need this if you set up your ordering on the model
        qs = super().get_queryset() 
        return qs.filter(user=self.request.user)


class TagGroupListOrganisationView(LoginRequiredMixin, CustomPermissionRequiredMixin, ListView):
    model = TagGroup
    template_name = "tag_group/tag_group_list.html"
    paginate_by = 10000
    permission_required = [('LIST', model.get_object_type(), None)]

    def get_queryset(self):
        qs = super().get_queryset() 
        return qs.filter(organisation__id=self.kwargs['organisation_id'])