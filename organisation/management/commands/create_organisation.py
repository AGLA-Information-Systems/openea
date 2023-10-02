from django.core.management.base import BaseCommand, CommandError
from authorization.controllers.utils import create_security_group_with_permissions, populate_permissions
from organisation.models import Organisation, Profile
from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils.translation import gettext as _

User = get_user_model()


class Command(BaseCommand):
    help = 'Create an organisation with its permissions'

    def add_arguments(self, parser):
        parser.add_argument('org_name', nargs=1, type=str)
        parser.add_argument('--superadmin', action='store_true')
        parser.add_argument('--users', nargs='*', type=str)

    def handle(self, *args, **options):
        superadmin = False
        if options['superadmin']:
            superadmin = True
        org_name = options['org_name'][0]
        users = options['users']

        populate_permissions()

        with transaction.atomic():
            try:
                print('org_name=', org_name)
                print('superadmin=', superadmin)
                print('users=', users)
                organisation, created = Organisation.objects.get_or_create(name=org_name, defaults={'description': ''})
                security_group_name = org_name + ' ' + _('Admin')
                admin_security_group = create_security_group_with_permissions(organisation=organisation, security_group_name=security_group_name, superadmin=superadmin)
                self.stdout.write(self.style.SUCCESS('Successfully created organisation "%s"' % org_name))
                for username in users:
                    user = User.objects.get(username=username)
                    user_profile, created = Profile.objects.get_or_create(organisation=organisation, user=user, defaults={'role': _('member')})
                    user_profile.is_active = True
                    user_profile.save()
                    admin_security_group.profiles.add(user_profile)
                admin_security_group.save()

            except Organisation.DoesNotExist:
                self.stdout.write(self.style.ERROR('Unable to created organisation "%s"' % org_name))
                raise CommandError('Organisation "%s" does not exist' % org_name)

        