import uuid
from django.forms import ValidationError

from django.test import TestCase
from django.urls import reverse

from authorization.models import Permission
from ontology.models import QUALITY_STATUS_PROPOSED, OConcept
from utils.test.helpers import (add_object_type_accesspermissions_to_security_group, create_accesspermission,
                                create_model, create_organisation,
                                create_repository, create_security_group,
                                create_user, create_user_profile)


class LoginTestCase(TestCase):
    def setUp(self):
        self.org_1 = create_organisation(name='Org 1', description='', location='test')
        self.org_1_user_1 = create_user(username='org_1_user_1')
        self.org_1_user_1_profile = create_user_profile(role='Admin', user=self.org_1_user_1, organisation=self.org_1)
        self.org_1_security_group_1 = create_security_group(name='Org 1 SecG 1', description='', organisation=self.org_1)
        self.org_1_security_group_1.profiles.add(self.org_1_user_1_profile)
        self.object_type = OConcept.get_object_type()

        self.org_1_user_2 = create_user(username='org_1_user_2')
        self.org_1_user_2_profile = create_user_profile(role='Admin', user=self.org_1_user_2, organisation=self.org_1)
        self.org_1_security_group_2 = create_security_group(name='Org 1 SecG 2', description='', organisation=self.org_1)
        self.org_1_security_group_2.profiles.add(self.org_1_user_2_profile)

        self.org_2 = create_organisation(name='Org 2', description='', location='test')


    def test_login_page_success(self):
        logged_in = self.client.login(username='org_1_user_1', password='12345')
        self.assertTrue(logged_in)

        logged_in = self.client.login(username='org_1_user_1', password='12345', organisation=self.org_1.name)
        self.assertTrue(logged_in)

        with self.assertRaises(ValidationError):
            logged_in = self.client.login(username='org_1_user_1', password='12345', organisation=self.org_2.name)
            self.assertFalse(logged_in)

