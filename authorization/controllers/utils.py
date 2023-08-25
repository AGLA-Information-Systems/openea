import traceback
from django.db import OperationalError, transaction
from openea.utils import DEFAULT_ACLS, OBJECT_TYPES_REGISTRY

from authorization.models import AccessPermission, Permission, SecurityGroup


def populate_permissions():
    with transaction.atomic():
        try:
            for object_type, cls in OBJECT_TYPES_REGISTRY.items():
                for action in cls.get_actions():
                    perm, created = Permission.objects.get_or_create(action=action, object_type=object_type)
                    DEFAULT_ACLS[object_type] = cls.get_actions()
        except OperationalError as e:
            traceback.print_exc()


def create_security_group_with_permissions(organisation, security_group_name, superadmin=False):
    admin_security_group, created = SecurityGroup.objects.get_or_create(name=security_group_name, organisation=organisation)
    perm_list = dict(DEFAULT_ACLS)
    for object_type, actions in perm_list.items():
        for action in actions:
            perm = Permission.objects.get(action=action, object_type=object_type)
            acl, created = AccessPermission.objects.get_or_create(permission=perm, organisation=organisation)
            acl.save()
            admin_security_group.accesspermissions.add(acl)
            admin_security_group.save()
    return admin_security_group
