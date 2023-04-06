from django.core.management.base import BaseCommand, CommandError
from authorization.controllers.utils import create_organisation_admin_security_group
from organisation.models import Organisation, Profile
from django.contrib.auth.models import User
from django.db import transaction

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
        with transaction.atomic():
            try:
                print('org_name=', org_name)
                print('superadmin=', superadmin)
                print('users=', users)
                organisation = Organisation.get_or_create(name=org_name, description='')
                admin_security_group_name = org_name + ' Admin Sec Group'
                admin_security_group = create_organisation_admin_security_group(organisation=organisation, admin_security_group_name=admin_security_group_name, superadmin=superadmin)
                self.stdout.write(self.style.SUCCESS('Successfully created organisation "%s"' % org_name))
                for username in users:
                    user = User.objects.get(username=username)
                    user_profile = Profile.get_or_create(organisation=organisation, user=user, role='employé')
                    user_profile.is_active = True
                    user_profile.save()
                    admin_security_group.profiles.add(user_profile)
                admin_security_group.save()

            except Organisation.DoesNotExist:
                self.stdout.write(self.style.ERROR('Unable to created organisation "%s"' % org_name))
                raise CommandError('Organisation "%s" does not exist' % org_name)

        