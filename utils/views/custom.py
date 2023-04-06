from django.http import Http404
from django.core.exceptions import PermissionDenied

from organisation.models import Organisation

class SingleObjectView:
    def get_object(self, **kwargs):
        obj = super().get_object(**kwargs)
        if self.request.user.is_staff:
            return obj
        if self.request.user.active_profile is not None:
            required_org = self.request.user.active_profile.organisation
            if isinstance(obj, Organisation) and obj == required_org:
                return obj
            if obj.organisation == required_org:
                return obj
        raise Http404()
    
    # def form_valid(self, form):
    #     if self.request.user.active_profile is None:
    #         raise PermissionDenied()
    #     if self.request.user.active_profile.organisation != form.instance.organisation:
    #         raise PermissionDenied()
    #     form.instance.modified_by = self.request.user
    #     return super().form_valid(form)
    
class MultipleObjectsView:
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        if self.request.user.is_staff:
            return qs
        if self.request.user.active_profile is not None:
            required_org = self.request.user.active_profile.organisation
            ids = [x.id for x in qs.all() if (isinstance(x, Organisation) and x == required_org) or (x.organisation == required_org)]
            return qs.filter(id__in=ids)
        return qs.none()