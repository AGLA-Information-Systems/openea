from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy, reverse
from authorization.controllers.utils import CustomPermissionRequiredMixin
from utils.views.custom import SingleObjectView

from organisation.models import Profile

class ProfileDeleteView(CustomPermissionRequiredMixin, SingleObjectView, DeleteView):
    model = Profile
    template_name = "profile/profile_delete.html"
    #success_url = reverse_lazy('profile_list')
    permission_required = [('DELETE', model.get_object_type(), None)]

    def get_success_url(self):
        pk = self.kwargs.get('organisation_id')
        return reverse('organisation_detail', kwargs={'pk': self.object.organisation.id})