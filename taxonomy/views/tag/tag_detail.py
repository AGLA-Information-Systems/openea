from django.views.generic import DetailView

from taxonomy.models import Tag
from django.contrib.auth.mixins import LoginRequiredMixin
from openea.utils import Utils

class TagDetailView(LoginRequiredMixin, DetailView):
    model = Tag
    template_name = "tag/tag_detail.html"
    permission_required = [(Utils.PERMISSION_ACTION_VIEW, model.get_object_type(), None)]
