from django.views.generic import ListView
from authorization.controllers.utils import CustomPermissionRequiredMixin

from ontology.models import OModel
from utils.views.custom import MultipleObjectsView, SingleObjectView

class OModelListView(CustomPermissionRequiredMixin, MultipleObjectsView, ListView):
    model = OModel
    template_name = "o_model/o_model_list.html"
    paginate_by = 10000
    permission_required = [('LIST', model.get_object_type(), None)]

    # def get_queryset(self):
    #     qs = super().get_queryset()
    #     repository_id=self.kwargs.get('repository_id')
    #     return qs.filter(repository_id__in=repository_id)
