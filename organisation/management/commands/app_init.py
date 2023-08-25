from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils.translation import gettext as _
from payment.controllers.products import populate_products
from authorization.controllers.utils import populate_permissions

class Command(BaseCommand):
    help = 'Create an organisation with its permissions'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        with transaction.atomic():
            try:
                print('Initializing permissions')
                populate_permissions()

                print('Initializing products')
                populate_products()
                
            except Exception as e:
                self.stdout.write(self.style.ERROR('Unable to proceed "%s"' % str(e)))
                raise CommandError(str(e))
    
