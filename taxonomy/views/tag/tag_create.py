from django.views.generic.edit import CreateView
from django.urls import reverse_lazy, reverse
from taxonomy.models import Tag
from authorization.controllers.utils import CustomPermissionRequiredMixin 
from django.contrib.auth.mixins import LoginRequiredMixin

class TagCreateView(LoginRequiredMixin, CustomPermissionRequiredMixin, CreateView):
    model = Tag
    fields = ['name', 'description', 'tag_group']
    template_name = "tag/tag_create.html"
    #success_url = reverse_lazy('tag_list')
    permission_required = [('CREATE', model.get_object_type(), None)]

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_initial(self):
        initials = super().get_initial()
        initials['user'] = self.request.user
        initials['tag_group'] = self.kwargs.get('tag_group_id')
        return initials

    def get_success_url(self):
        pk = self.kwargs.get('tag_group_id')
        return reverse('tag_group_detail', kwargs={'pk': self.object.tag_group.id})