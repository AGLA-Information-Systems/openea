from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy, reverse
from datetime import datetime
from taxonomy.models import Tag
from authorization.controllers.utils import CustomPermissionRequiredMixin, create_organisation_admin_security_group
from django.contrib.auth.mixins import LoginRequiredMixin

class TagUpdateView(LoginRequiredMixin, CustomPermissionRequiredMixin, UpdateView):
    model = Tag
    fields = ['name', 'description', 'tag_group']
    template_name = "tag/tag_update.html"
    #success_url = reverse_lazy('tag_list')
    permission_required = [('UPDATE', model.get_object_type(), None)]

    def form_valid(self, form):
        form.instance.modified_by = self.request.user
        form.instance.modified_at = datetime.now()
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.kwargs.get('tag_group_id')
        return reverse('tag_group_detail', kwargs={'pk': self.object.tag_group.id})