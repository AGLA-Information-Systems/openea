from typing import  Dict
from authorization.models import AccessPermission, Permission

from django.core.exceptions import PermissionDenied


class AclDenied(PermissionDenied):
    def __init__(self, message, **extra):
        self.message = message
        self.detail = {'message': message}
        self.detail.update(**extra)
    
    def __str__(self):
        return "{}".format(self.message)

class Acl:
    def __init__(self, user):
        self.user = user

    def __str__(self):
        return '<Acl id: %s>' % self.id

    def check(self, organisation, permissions_required):
        if isinstance(permissions_required, tuple):
            permissions_required = [permissions_required]
        can_access = False

        try:
            accesspermissions_required = self.get_accesspermissions(organisation=organisation, permissions_required=permissions_required)
        except AclDenied as e:
            return can_access
        user_security_groups = self.user.active_profile.security_groups.filter(organisation=organisation)
        
        for security_group in user_security_groups.all():
            access_perms = set(security_group.accesspermissions.all())
            can_access = all([x in access_perms for x in accesspermissions_required])
            if can_access:
                break
        return can_access

    def check_raise(self, organisation, permissions_required):
        if not self.check(organisation=organisation, permissions_required=permissions_required):
            raise AclDenied('User {} does not have access permissions {} for organisation'.format(self.user, permissions_required), extra={'organisation': organisation})
        return True

    def get_accesspermissions(self, organisation, permissions_required):
        perms = []
        if len(permissions_required) > 0:
            if organisation is None:
                raise AclDenied('Organisation not selected')
            for perm in permissions_required:
                system_perms = Permission.objects.filter(action=perm[0], object_type=perm[1])
                for x in AccessPermission.objects.filter(organisation=organisation, permission__in=system_perms, object_identifier=perm[2]):
                        perms.append(x)
            if len(perms) == 0:
                raise AclDenied('Organisation {} does not have permission : {}'.format(organisation.name, perm), extra={'organisation': organisation})
        return set(perms)
