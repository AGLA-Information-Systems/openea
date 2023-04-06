from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy, reverse
from authorization.controllers.utils import CustomPermissionRequiredMixin
from utils.views.custom import SingleObjectView

from organisation.models import Profile

class ProfileUpdateView(CustomPermissionRequiredMixin, SingleObjectView, UpdateView):
    model = Profile
    fields = ['role', 'description']
    template_name = "profile/profile_update.html"
    #success_url = reverse_lazy('profile_list')
    permission_required = [('UPDATE', model.get_object_type(), None)]

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.modified_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.kwargs.get('organisation_id')
        return reverse('organisation_detail', kwargs={'pk': self.object.organisation.id})