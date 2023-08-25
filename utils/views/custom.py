from django.http import Http404
from django.core.exceptions import ImproperlyConfigured
from urllib.parse import urlparse
from organisation.models import Organisation
from django.views.generic.edit import CreateView


class ReferrerView:
    """
    Master view class that provides default functions.
    """
    organisation = None
    permission_required = []

    def get_permission_required(self):
        """
        Override this method to override the permission_required attribute.
        Must return an iterable.
        """
        if self.permission_required is None:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} is missing the "
                f"permission_required attribute. Define "
                f"{self.__class__.__name__}.permission_required, or override "
                f"{self.__class__.__name__}.get_permission_required()."
            )
        if isinstance(self.permission_required, tuple):
            perms = [self.permission_required]
        else:
            perms = self.permission_required
        return perms

    def get_target_organisation(self, *args, **kwargs):
        if self.organisation is None and self.request.user.is_authenticated and self.request.user.active_profile is not None:
            self.organisation = self.request.user.active_profile.organisation
        return self.organisation

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        full_url = self.request.META.get('HTTP_REFERER')
        parsed = urlparse(full_url)
        context["return_url"] = full_url
        context["return_path"] = parsed.path
        self.return_url = full_url
        return context
    
    def dispatch(self, request, *args, **kwargs):
        permissions_required = self.get_permission_required()
        if permissions_required:
            self.get_target_organisation()
            request.acl.check_raise(organisation=self.organisation, permissions_required=permissions_required)
        self.request.view = self
        return super().dispatch(request, *args, **kwargs)

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
    #     form.instance.modified_at = timezone.now()
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
        #check payment access
        
        return super(CustomCreateView, self).post(request, *args, **kwargs)
