import uuid

from django.test import TestCase
from django.urls import reverse

from authorization.models import Permission
from utils.test.helpers import (add_object_type_permissions_to_security_group,
                                create_organisation, create_security_group,
                                create_user, create_user_profile)
from organisation.models import Profile


class ProfileCreateTestCase(TestCase):
    def setUp(self):
        self.org_1 = create_organisation(name='Org 1', description='', location='test')
        self.org_1_user_1 = create_user(username='org_1_user_1')
        self.org_1_user_1_profile = create_user_profile(role='Admin', user=self.org_1_user_1, organisation=self.org_1)
        self.org_1_security_group_1 = create_security_group(name='Org 1 SecG 1', description='', organisation=self.org_1)
        self.org_1_security_group_1.profiles.add(self.org_1_user_1_profile)
        self.object_type = Profile.get_object_type()
        add_object_type_permissions_to_security_group(organisation=self.org_1, security_group=self.org_1_security_group_1, object_type=self.object_type)

        self.org_1_user_2 = create_user(username='org_1_user_2')
        
        
    def test_profile_create_page_not_authenticated(self):
        bogus_uuid = uuid.uuid4()
        response = self.client.get(reverse('profile_create', kwargs={'organisation_id': bogus_uuid}))
        self.assertRedirects(response, '/user/login/?redirect_to=/profile/create/'+ str(bogus_uuid) +'/', status_code=302, target_status_code=200, fetch_redirect_response=True)
        response = self.client.post(reverse('profile_create', kwargs={'organisation_id': bogus_uuid}), data={})
        self.assertRedirects(response, '/user/login/?redirect_to=/profile/create/'+ str(bogus_uuid) +'/', status_code=302, target_status_code=200, fetch_redirect_response=True)
        
    def test_profile_create_page_authenticated_not_allowed(self):
        bogus_uuid = uuid.uuid4()
        logged_in = self.client.login(username='org_1_user_1', password='12345')
        self.assertTrue(logged_in)
        response = self.client.get(reverse('profile_create', kwargs={'organisation_id': bogus_uuid}))
        self.assertEqual(response.status_code, 403)
        response = self.client.post(reverse('profile_create', kwargs={'organisation_id': bogus_uuid}), data={})
        self.assertEqual(response.status_code, 403)

        response = self.client.get(reverse('profile_create', kwargs={'organisation_id': self.org_1.id}))
        self.assertEqual(response.status_code, 403)
        response = self.client.post(reverse('profile_create', kwargs={'organisation_id': self.org_1.id}), data={})
        self.assertEqual(response.status_code, 403)

    def test_profile_create_page_success(self):
        logged_in = self.client.login(username='org_1_user_1', password='12345')
        self.assertTrue(logged_in)
        self.assertTrue(self.org_1_user_1.profiles.filter(id=self.org_1_user_1_profile.id).exists())
        self.assertTrue(not hasattr(self.org_1_user_1, 'active_profile'))
        response = self.client.post(reverse('profile_activate', kwargs={'pk':str(self.org_1_user_1_profile.id)}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.org_1_user_1_profile.organisation == self.org_1)
        self.assertTrue(self.org_1_user_1_profile.security_groups.filter(id=self.org_1_security_group_1.id).exists())
        
        for perm in Permission.objects.filter(organisation=self.org_1, action='CREATE', object_type=self.object_type):
            print(perm)

        required_permission = Permission.objects.get(organisation=self.org_1, action='CREATE', object_type=self.object_type)
        self.assertIsNotNone(required_permission)
        perms = [str(x) for x in self.org_1_security_group_1.permissions.all()]
        self.assertTrue(self.org_1_security_group_1.permissions.filter(id=required_permission.id).exists())

        response = self.client.get(reverse('profile_create', kwargs={'organisation_id': self.org_1.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile/profile_create.html')
        response = self.client.post(reverse('profile_create', kwargs={'organisation_id': self.org_1.id}), data={'name':'Profile 1', 'description': ''})
        self.assertEqual(response.status_code, 200) #TODO : Not 200 in case of error
        response = self.client.post(reverse('profile_create', kwargs={'organisation_id': self.org_1.id}), data={'role':'Admin 1', 'description': '', 'user': self.org_1_user_2.id, 'organisation': self.org_1.id})
        self.assertEqual(response.status_code, 302, response.content)
        response = self.client.post(reverse('profile_create', kwargs={'organisation_id': self.org_1.id}), data={'role':'Architect', 'description': '', 'user': self.org_1_user_1.id, 'organisation': self.org_1.id})
        self.assertEqual(response.status_code, 302, response.content)

        self.client.logout()

        self.org_1_user_2_profile = Profile.objects.get(user=self.org_1_user_2, organisation=self.org_1.id)
        self.org_1_security_group_2 = create_security_group(name='Org 1 SecG 2', description='', organisation=self.org_1)
        self.org_1_security_group_2.profiles.add(self.org_1_user_2_profile)

        response = self.client.get(reverse('profile_create', kwargs={'organisation_id': self.org_1.id}))
        self.assertRedirects(response, '/user/login/?redirect_to=/profile/create/'+ str(self.org_1.id) +'/', status_code=302, target_status_code=200, fetch_redirect_response=True)

        logged_in = self.client.login(username='org_1_user_2', password='12345')
        self.assertTrue(logged_in)
        response = self.client.get(reverse('profile_create', kwargs={'organisation_id': self.org_1.id}))
        self.assertEqual(response.status_code, 403)
        response = self.client.post(reverse('profile_create', kwargs={'organisation_id': self.org_1.id}), data={})
        self.assertEqual(response.status_code, 403)