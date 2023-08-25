from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy, reverse

from taxonomy.models import Tag

from django.contrib.auth.mixins import LoginRequiredMixin
from openea.utils import Utils

class TagDeleteView(LoginRequiredMixin, DeleteView):
    model = Tag
    template_name = "tag/tag_delete.html"
    #success_url = reverse_lazy('tag_list')
    permission_required = [(Utils.PERMISSION_ACTION_DELETE, model.get_object_type(), None)]

    def get_success_url(self):
        pk = self.kwargs.get('organisation_id')
        return reverse('organisation_detail', kwargs={'pk': self.object.organisation.id})