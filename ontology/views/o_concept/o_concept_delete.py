from django.urls import reverse, reverse_lazy
from django.views.generic.edit import DeleteView
from django.core.exceptions import PermissionDenied
from authorization.controllers.utils import CustomPermissionRequiredMixin, create_organisation_admin_security_group
from django.contrib.auth.mixins import LoginRequiredMixin
from ontology.models import OConcept
from utils.views.custom import SingleObjectView

__author__ = "Patrick Agbokou"
__copyright__ = "Copyright 2021, OpenEA"
__credits__ = ["Patrick Agbokou"]
__license__ = "Apache License 2.0"
__version__ = "1.0.0"
__maintainer__ = "Patrick Agbokou"
__email__ = "patrick.agbokou@aglaglobal.com"
__status__ = "Development"

class OConceptDeleteView(CustomPermissionRequiredMixin, SingleObjectView, DeleteView):
    model = OConcept
    template_name = "o_concept/o_concept_delete.html"
    #success_url = reverse_lazy('o_concept_list')
    permission_required = [('DELETE', model.get_object_type(), None)]

    def get_success_url(self):
        pk = self.object.model.id
        return reverse('o_model_detail', kwargs={'pk': pk})