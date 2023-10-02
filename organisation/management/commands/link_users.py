from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils.translation import gettext as _
from authorization.models import SecurityGroup
from organisation.models import Organisation, Profile

User = get_user_model()


class Command(BaseCommand):
    help = 'Create an organisation with its permissions'

    def add_arguments(self, parser):
        parser.add_argument('org_name', nargs=1, type=str)
        parser.add_argument('--security_group', nargs=1, type=str)
        parser.add_argument('--role', nargs=1, type=str)
        parser.add_argument('--users', nargs='*', type=str)

    def handle(self, *args, **options):
        org_name = options['org_name'][0]
        security_group_name = options['security_group'][0]
        role = options['role'][0] or _('member')
        users = options['users']
        with transaction.atomic():
            try:
                print('org_name=', org_name)
                print('security_group=', security_group_name)
                print('role=', role)
                print('users=', users)
                organisation = Organisation.objects.get(name=org_name)
                security_group = SecurityGroup.objects.get(organisation=organisation, name=security_group_name)
                for username in users:
                    try:
                        user = User.objects.get(username=username)
                    except User.DoesNotExist:
                        password = User.objects.make_random_password()
                        user = User.objects.create(username=username)
                        user.set_password(password)
                        user.save()
                        self.stdout.write(self.style.SUCCESS('Successfully created user "%s" "%s" ' % (username, password)))

                    user_profile, created = Profile.objects.get_or_create(organisation=organisation, user=user, role=role)
                    user_profile.is_active = True
                    user_profile.save()
                    security_group.profiles.add(user_profile)
                security_group.save()
                self.stdout.write(self.style.SUCCESS('Successfully linked users to "%s"' % org_name))
            except SecurityGroup.DoesNotExist:
                self.stdout.write(self.style.ERROR('Unable to find security group "%s"' % security_group_name))
            except Organisation.DoesNotExist:
                self.stdout.write(self.style.ERROR('Unable to find organisation "%s"' % org_name))
                raise CommandError('Organisation "%s" does not exist' % org_name)
