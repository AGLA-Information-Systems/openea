from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy, reverse

from django.contrib.auth.mixins import LoginRequiredMixin
from openea.utils import Utils
from utils.views.custom import SingleObjectView
from django.utils import timezone
from organisation.models import Organisation

class OrganisationUpdateView(LoginRequiredMixin, SingleObjectView, UpdateView):
    model = Organisation
    fields = ['name', 'description', 'location']
    template_name = "organisation/organisation_update.html"
    success_url = reverse_lazy('organisation_list')
    permission_required = [('UPDATE', model.get_object_type(), None)]

    def form_valid(self, form):
        form.instance.modified_by = self.request.user
        form.instance.modified_at = timezone.now()
        return super().form_valid(form)
