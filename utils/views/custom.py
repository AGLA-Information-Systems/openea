from django.http import Http404
from django.core.exceptions import PermissionDenied
from urllib.parse import urlparse
from organisation.models import Organisation
from datetime import datetime
from django.views.generic.edit import CreateView


class ReferrerView:
    organisation = None

    def get_current_organisation(self, request, *args, **kwargs):
        if hasattr(self, 'object') and self.object is not None:
            self.organisation = self.object.get_organsiation()
            object_id = str(self.object.id)
        if self.organisation is None and self.request.user.is_authenticated and self.request.user.active_profile is not None:
            self.organisation = self.request.user.active_profile.organisation
        return super(ReferrerView, self).post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        full_url = self.request.META.get('HTTP_REFERER')
        parsed = urlparse(full_url)
        context["return_url"] = full_url
        context["return_path"] = parsed.path
        self.return_url = full_url
        return context

class SingleObjectView (ReferrerView):
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
    #     form.instance.modified_at = datetime.now()
    #     return super().form_valid(form)
    
class MultipleObjectsView (ReferrerView):
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        if self.request.user.is_staff:
            return qs
        if self.request.user.active_profile is not None:
            required_org = self.request.user.active_profile.organisation
            ids = [x.id for x in qs.all() if (isinstance(x, Organisation) and x == required_org) or (x.organisation == required_org)]
            return qs.filter(id__in=ids)
        return qs.none()
    

class CustomCreateView(ReferrerView, CreateView):
    def post(self, request, *args, **kwargs):
        self.object = None
        #check access
        self.get_current_organisation(request, *args, **kwargs)

        return super(CustomCreateView, self).post(request, *args, **kwargs)
