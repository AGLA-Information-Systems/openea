from django.views.generic.edit import CreateView
from django.urls import reverse_lazy, reverse
from authorization.controllers.utils import CustomPermissionRequiredMixin

from organisation.models import Profile
from webapp.forms import ProfileCreateForm

class ProfileCreateView(CustomPermissionRequiredMixin, CreateView):
    model = Profile
    # fields = ['role', 'description', 'user', 'organisation']
    template_name = "profile/profile_create.html"
    form_class = ProfileCreateForm
    #success_url = reverse_lazy('profile_list')
    permission_required = [('CREATE', model.get_object_type(), None)]

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_initial(self):
        initials = super().get_initial()
        initials['user'] = self.request.user
        initials['organisation'] = self.kwargs.get('organisation_id')
        return initials

    def get_success_url(self):
        pk = self.kwargs.get('organisation_id')
        return reverse('organisation_detail', kwargs={'pk': self.object.organisation.id})