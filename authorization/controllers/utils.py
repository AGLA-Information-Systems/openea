from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from openea.utils import Utils

from ..models import Permission, SecurityGroup

DEFAULT_PERMISSIONS = {
    Utils.OBJECT_ORGANISATION: [Permission.PERMISSION_ACTION_LIST, Permission.PERMISSION_ACTION_VIEW],
    Utils.OBJECT_PERMISSION: [Permission.PERMISSION_ACTION_CREATE, Permission.PERMISSION_ACTION_LIST, Permission.PERMISSION_ACTION_VIEW, Permission.PERMISSION_ACTION_UPDATE, Permission.PERMISSION_ACTION_DELETE],
    Utils.OBJECT_SECURITY_GROUP: [Permission.PERMISSION_ACTION_CREATE, Permission.PERMISSION_ACTION_LIST, Permission.PERMISSION_ACTION_VIEW, Permission.PERMISSION_ACTION_UPDATE, Permission.PERMISSION_ACTION_DELETE],
    Utils.OBJECT_PROFILE: [Permission.PERMISSION_ACTION_CREATE, Permission.PERMISSION_ACTION_LIST, Permission.PERMISSION_ACTION_VIEW, Permission.PERMISSION_ACTION_UPDATE, Permission.PERMISSION_ACTION_DELETE],
    Utils.OBJECT_PERMISSION: [Permission.PERMISSION_ACTION_CREATE, Permission.PERMISSION_ACTION_LIST, Permission.PERMISSION_ACTION_VIEW, Permission.PERMISSION_ACTION_UPDATE, Permission.PERMISSION_ACTION_DELETE],
    Utils.OBJECT_SECURITY_GROUP: [Permission.PERMISSION_ACTION_CREATE, Permission.PERMISSION_ACTION_LIST, Permission.PERMISSION_ACTION_VIEW, Permission.PERMISSION_ACTION_UPDATE, Permission.PERMISSION_ACTION_DELETE],
    Utils.OBJECT_TASK: [Permission.PERMISSION_ACTION_CREATE, Permission.PERMISSION_ACTION_LIST, Permission.PERMISSION_ACTION_VIEW, Permission.PERMISSION_ACTION_UPDATE, Permission.PERMISSION_ACTION_DELETE],
    Utils.OBJECT_REPOSITORY: [Permission.PERMISSION_ACTION_CREATE, Permission.PERMISSION_ACTION_LIST, Permission.PERMISSION_ACTION_VIEW, Permission.PERMISSION_ACTION_UPDATE, Permission.PERMISSION_ACTION_DELETE],
    Utils.OBJECT_MODEL: [Permission.PERMISSION_ACTION_CREATE, Permission.PERMISSION_ACTION_LIST, Permission.PERMISSION_ACTION_VIEW, Permission.PERMISSION_ACTION_UPDATE, Permission.PERMISSION_ACTION_DELETE, Permission.PERMISSION_ACTION_EXPORT, Permission.PERMISSION_ACTION_IMPORT],
    Utils.OBJECT_CONCEPT: [Permission.PERMISSION_ACTION_CREATE, Permission.PERMISSION_ACTION_LIST, Permission.PERMISSION_ACTION_VIEW, Permission.PERMISSION_ACTION_UPDATE, Permission.PERMISSION_ACTION_DELETE],
    Utils.OBJECT_RELATION: [Permission.PERMISSION_ACTION_CREATE, Permission.PERMISSION_ACTION_LIST, Permission.PERMISSION_ACTION_VIEW, Permission.PERMISSION_ACTION_UPDATE, Permission.PERMISSION_ACTION_DELETE],
    Utils.OBJECT_PREDICATE: [Permission.PERMISSION_ACTION_CREATE, Permission.PERMISSION_ACTION_LIST, Permission.PERMISSION_ACTION_VIEW, Permission.PERMISSION_ACTION_UPDATE, Permission.PERMISSION_ACTION_DELETE],
    Utils.OBJECT_INSTANCE: [Permission.PERMISSION_ACTION_CREATE, Permission.PERMISSION_ACTION_LIST, Permission.PERMISSION_ACTION_VIEW, Permission.PERMISSION_ACTION_UPDATE, Permission.PERMISSION_ACTION_DELETE],
    Utils.OBJECT_REPORT: [Permission.PERMISSION_ACTION_CREATE, Permission.PERMISSION_ACTION_LIST, Permission.PERMISSION_ACTION_VIEW, Permission.PERMISSION_ACTION_UPDATE, Permission.PERMISSION_ACTION_DELETE, Permission.PERMISSION_ACTION_RUN],
    Utils.OBJECT_TAG_GROUP: [Permission.PERMISSION_ACTION_CREATE, Permission.PERMISSION_ACTION_LIST, Permission.PERMISSION_ACTION_VIEW, Permission.PERMISSION_ACTION_UPDATE, Permission.PERMISSION_ACTION_DELETE],
    Utils.OBJECT_TAG: [Permission.PERMISSION_ACTION_CREATE, Permission.PERMISSION_ACTION_LIST, Permission.PERMISSION_ACTION_VIEW, Permission.PERMISSION_ACTION_UPDATE, Permission.PERMISSION_ACTION_DELETE],
    Utils.OBJECT_LOG: [Permission.PERMISSION_ACTION_CREATE, Permission.PERMISSION_ACTION_LIST, Permission.PERMISSION_ACTION_VIEW, Permission.PERMISSION_ACTION_UPDATE, Permission.PERMISSION_ACTION_DELETE],
    Utils.OBJECT_CONFIG: [Permission.PERMISSION_ACTION_CREATE, Permission.PERMISSION_ACTION_LIST, Permission.PERMISSION_ACTION_VIEW, Permission.PERMISSION_ACTION_UPDATE, Permission.PERMISSION_ACTION_DELETE]
}

def authorization_required(function, action, object_type):
    def wrapper(*args,**kwargs):
        request = kwargs.get('request')
        user = request.user

        check_permission(user, action, object_type, object_identifier=None)
        try:
            return function(*args,**kwargs)
        except Exception as e:
            return HttpResponse('Exception:'+str(e))
    return wrapper

def check_permission(user, action, object_type, object_identifier=None):
    for profile in user.profiles.all():
        for security_group in profile.security_groups.all():
            if security_group.permissions.filter(action=action, object_type=object_type, object_identifier=object_identifier).count() > 0:
                return True
    return False

def create_organisation_admin_security_group(organisation, admin_security_group_name, superadmin=False):
    admin_security_group = SecurityGroup.get_or_create(name=admin_security_group_name, organisation=organisation)
    perm_list = dict(DEFAULT_PERMISSIONS)
    if superadmin:
        perm_list[Utils.OBJECT_ORGANISATION] = perm_list[Utils.OBJECT_ORGANISATION] + [Permission.PERMISSION_ACTION_CREATE, Permission.PERMISSION_ACTION_UPDATE, Permission.PERMISSION_ACTION_DELETE]
    for object_type, actions in perm_list.items():
        for action in actions:
            perm = Permission.get_or_create(action=action, object_type=object_type, organisation=organisation)
            perm.security_groups.add(admin_security_group)
            perm.save()
    return admin_security_group


class CustomPermissionRequiredMixin(LoginRequiredMixin, PermissionRequiredMixin):
    """Verify that the current user has all specified permissions."""
    login_url = '/user/login/'
    redirect_field_name = 'redirect_to'
    permission_required = None

    def get_permission_required(self):
        """
        Override this method to override the permission_required attribute.
        Must return an iterable.
        """
        if self.permission_required is None:
            raise ValueError(
                f"{self.__class__.__name__} is missing the "
                f"permission_required attribute. Define "
                f"{self.__class__.__name__}.permission_required, or override "
                f"{self.__class__.__name__}.get_permission_required()."
            )
        
        object_id = None
        organisation = None
        if hasattr(self, 'object') and self.object is not None:
            organisation = self.object.get_organsiation()
            object_id = str(self.object.id)
        if organisation is None and self.request.user.active_profile is not None:
            organisation = self.request.user.active_profile.organisation
            
        perms = []
        for perm in self.permission_required:
            try:
                if Permission.objects.get(organisation=organisation, action=perm[0], object_type=perm[1], object_identifier=perm[2]):
                    perms.append(perm) 
            except Exception as e:
                raise PermissionDenied('Missing Permission: {} - {}'.format(perm, str(e)))   
        return set(perms)

    def has_permission(self):
        """
        Override this method to customize the way permissions are checked.
        """
        perms_required = self.get_permission_required()
        user_perms = []
        if not perms_required:
            return True
        has_perm = False
        for profile in self.request.user.profiles.all():
            for security_group in profile.security_groups.all():
                user_perms = user_perms + [(perm.action, perm.object_type, perm.object_identifier) for perm in security_group.permissions.all()]
        user_perms = set(user_perms)
        for perm in perms_required:
            has_perm = has_perm or (perm in user_perms)
        return has_perm

    # def dispatch(self, request, *args, **kwargs):
    #     if not self.request.user.is_authenticated:
    #         return self.handle_no_permission()
    #     if not self.has_permission():
    #         return self.handle_no_permission()
    #     return super().dispatch(request, *args, **kwargs)
