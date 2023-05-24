import uuid
from django.test import TestCase
from django.urls import reverse
from ontology.models import OModel

from utils.test.helpers import add_object_type_permissions_to_security_group, create_model, create_organisation, create_repository, create_security_group, create_user, create_user_profile


class InstanceImportTestCase(TestCase):
    def setUp(self):
        self.org_1 = create_organisation(name='Org 1', description='', location='test')
        self.org_1_user_1 = create_user(username='org_1_user_1')
        self.org_1_user_1_profile = create_user_profile(role='Admin', user=self.org_1_user_1, organisation=self.org_1)
        self.org_1_security_group_1 = create_security_group(name='Org 1 SecG 1', description='', organisation=self.org_1)
        self.org_1_security_group_1.profiles.add(self.org_1_user_1_profile)
        self.object_type = OModel.get_object_type()
        add_object_type_permissions_to_security_group(organisation=self.org_1, security_group=self.org_1_security_group_1, object_type=self.object_type)

        self.org_1_repo = create_repository(organisation=self.org_1, name='org_1_repo_1')
        self.org_1_model = create_model(repository=self.org_1_repo, name='org_1_model_1')

    def test_import_view_page_not_authenticated(self):
        bogus_uuid = uuid.uuid4()
        response = self.client.get(reverse('model_import', kwargs={'model_id': bogus_uuid}))
        self.assertRedirects(response, '/user/login/?redirect_to=/model_import/' + str(bogus_uuid) + '/', status_code=302, target_status_code=200, fetch_redirect_response=True)
        response = self.client.post(reverse('model_import', kwargs={'model_id': bogus_uuid}), data={})
        self.assertRedirects(response, '/user/login/?redirect_to=/model_import/' + str(bogus_uuid) + '/', status_code=302, target_status_code=200, fetch_redirect_response=True)

    def test_import_view_page_authenticated_not_allowed(self):
        bogus_uuid = uuid.uuid4()
        login = self.client.login(username='org_1_user_1', password='12345')
        self.assertTrue(login)
        response = self.client.get(reverse('model_import', kwargs={'model_id': bogus_uuid}))
        self.assertEqual(response.status_code, 403)
        response = self.client.post(reverse('model_import', kwargs={'model_id': bogus_uuid}), data={})
        self.assertEqual(response.status_code, 403)

    def test_import_view_page_authenticated_success(self):
        # log the user in
        login = self.client.login(username='org_1_user_1', password='12345')
        self.assertTrue(login)
        self.assertTrue(self.org_1_user_1.profiles.filter(id=self.org_1_user_1_profile.id).exists())
        self.assertTrue(not hasattr(self.org_1_user_1, 'active_profile'))
        response = self.client.post(reverse('profile_activate', kwargs={'pk':str(self.org_1_user_1_profile.id)}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.org_1_user_1_profile.organisation == self.org_1)
        self.assertTrue(self.org_1_user_1_profile.security_groups.filter(id=self.org_1_security_group_1.id).exists())

        response = self.client.get(reverse('model_import', kwargs={'model_id': self.org_1_model.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'model_import.html')
        response = self.client.post(reverse('model_import', kwargs={'model_id': self.org_1_model.id}), data={
            'file': open('ontology/tests/import_export/instance_import_test.json', 'rb')
        })
        self.assertEqual(response.status_code, 200)
