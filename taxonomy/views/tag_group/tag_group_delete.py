from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy, reverse

from taxonomy.models import TagGroup
from authorization.controllers.utils import CustomPermissionRequiredMixin

class TagGroupDeleteView(CustomPermissionRequiredMixin, DeleteView):
    model = TagGroup
    template_name = "tag_group/tag_group_delete.html"
    #success_url = reverse_lazy('tag_group_list')
    permission_required = [('DELETE', model.get_object_type(), None)]

    def get_success_url(self):
        pk = self.kwargs.get('organisation_id')
        return reverse('organisation_detail', kwargs={'pk': self.object.organisation.id})