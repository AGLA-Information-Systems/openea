from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy, reverse
from authorization.controllers.utils import CustomPermissionRequiredMixin

from webapp.models import Organisation

class OrganisationUpdateView(CustomPermissionRequiredMixin, UpdateView):
    model = Organisation
    fields = ['name', 'description', 'location']
    template_name = "organisation/organisation_update.html"
    success_url = reverse_lazy('organisation_list')
    permission_required = [('UPDATE', model.get_object_type(), None)]

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.modified_by = self.request.user
        return super().form_valid(form)
