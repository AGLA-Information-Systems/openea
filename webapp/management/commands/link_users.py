from django.core.management.base import BaseCommand, CommandError
from authorization.models import SecurityGroup
from webapp.models import Organisation, Profile
from django.contrib.auth.models import User
from django.db import transaction

class Command(BaseCommand):
    help = 'Create an organisation with its permissions'

    def add_arguments(self, parser):
        parser.add_argument('org_name', nargs=1, type=str)
        parser.add_argument('security_group_name', nargs=1, type=str)
        parser.add_argument('--users', nargs='*', type=str)

    def handle(self, *args, **options):
        org_name = options['org_name'][0]
        security_group_name = options['security_group_name'][0]
        users = options['users']
        with transaction.atomic():
            try:
                print('org_name=', org_name)
                print('security_group_name=', security_group_name)
                print('users=', users)
                organisation = Organisation.objects.get(name=org_name)
                security_group = SecurityGroup.objects.get(organisation=organisation, name=security_group_name)
                
                for username in users:
                    user = User.objects.get(username=username)
                    user_profile = Profile.get_or_create(organisation=organisation, user=user, role='employé')
                    user_profile.is_active = False
                    user_profile.save()
                    security_group.profiles.add(user_profile)
                security_group.save()
                self.stdout.write(self.style.SUCCESS('Successfully linked users to "%s"' % org_name))
            except SecurityGroup.DoesNotExist:
                self.stdout.write(self.style.ERROR('Unable to find security group "%s"' % security_group_name))
            except Organisation.DoesNotExist:
                self.stdout.write(self.style.ERROR('Unable to find organisation "%s"' % org_name))
                raise CommandError('Organisation "%s" does not exist' % org_name)
