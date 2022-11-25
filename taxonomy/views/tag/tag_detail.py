from django.views.generic import DetailView

from taxonomy.models import Tag
from authorization.controllers.utils import CustomPermissionRequiredMixin


class TagDetailView(CustomPermissionRequiredMixin, DetailView):
    model = Tag
    template_name = "tag/tag_detail.html"
    permission_required = [('VIEW', model.get_object_type(), None)]
