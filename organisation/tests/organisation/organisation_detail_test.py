import uuid

from django.test import TestCase
from django.urls import NoReverseMatch, reverse

from authorization.models import Permission
from ontology.models import Organisation
from utils.test.helpers import (create_organisation, create_accesspermission,
                                create_security_group, create_user,
                                create_user_profile)


class OrganisationDetailTestCase(TestCase):
    def setUp(self):
        self.org_1 = create_organisation(name='Org 1', description='', location='test')
        self.org_1_user_1 = create_user(username='org_1_user_1')
        self.org_1_user_1_profile = create_user_profile(role='Admin', user=self.org_1_user_1, organisation=self.org_1)
        self.org_1_security_group_1 = create_security_group(name='Org 1 SecG 1', description='', organisation=self.org_1)
        self.org_1_security_group_1.profiles.add(self.org_1_user_1_profile)
        self.object_type = Organisation.get_object_type()
        self.perm = create_accesspermission(security_group=self.org_1_security_group_1, action='VIEW', object_type=self.object_type)

        self.org_1_user_2 = create_user(username='org_1_user_2')
        self.org_1_user_2_profile = create_user_profile(role='Admin', user=self.org_1_user_2, organisation=self.org_1)
        self.org_1_security_group_2 = create_security_group(name='Org 1 SecG 2', description='', organisation=self.org_1)
        self.org_1_security_group_2.profiles.add(self.org_1_user_2_profile)

        
    def test_organisation_detail_page_not_authenticated(self):
        with self.assertRaises(NoReverseMatch):
            response = self.client.get(reverse('organisation_detail'))
        bogus_uuid = uuid.uuid4()
        response = self.client.get(reverse('organisation_detail', kwargs={'pk': bogus_uuid}))
        self.assertRedirects(response, '/user/login/?next=/organisation/detail/'+ str(bogus_uuid) +'/', status_code=302, target_status_code=200, fetch_redirect_response=True)
        response = self.client.get(reverse('organisation_detail', kwargs={'pk': self.org_1.id}))
        self.assertRedirects(response, '/user/login/?next=/organisation/detail/' + str(self.org_1.id) +'/', status_code=302, target_status_code=200, fetch_redirect_response=True)
        response = self.client.post(reverse('organisation_detail', kwargs={'pk': self.org_1.id}), data={})
        self.assertRedirects(response, '/user/login/?next=/organisation/detail/' + str(self.org_1.id) +'/', status_code=302, target_status_code=200, fetch_redirect_response=True)
        
    def test_organisation_detail_page_authenticated_not_allowed(self):
        bogus_uuid = uuid.uuid4()
        logged_in = self.client.login(username='org_1_user_1', password='12345')
        self.assertTrue(logged_in)
        response = self.client.get(reverse('organisation_detail', kwargs={'pk': bogus_uuid}))
        self.assertEqual(response.status_code, 403)
        response = self.client.post(reverse('organisation_detail', kwargs={'pk': bogus_uuid}), data={})
        self.assertEqual(response.status_code, 403)
        response = self.client.get(reverse('organisation_detail', kwargs={'pk': self.org_1.id}))
        self.assertEqual(response.status_code, 403)
        response = self.client.post(reverse('organisation_detail', kwargs={'pk': self.org_1.id}), data={})
        self.assertEqual(response.status_code, 403)

    def test_organisation_detail_page_success(self):
        logged_in = self.client.login(username='org_1_user_1', password='12345')
        self.assertTrue(logged_in)
        self.assertTrue(self.org_1_user_1.profiles.filter(id=self.org_1_user_1_profile.id).exists())
        self.assertTrue(not hasattr(self.org_1_user_1, 'active_profile'))
        response = self.client.post(reverse('profile_activate', kwargs={'pk':str(self.org_1_user_1_profile.id)}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.org_1_user_1_profile.organisation == self.org_1)
        self.assertTrue(self.org_1_user_1_profile.security_groups.filter(id=self.org_1_security_group_1.id).exists())
        
        create_accesspermission(security_group=self.org_1_security_group_1, action='VIEW', object_type=self.object_type)

        with self.assertRaises(NoReverseMatch):
            response = self.client.get(reverse('organisation_detail'))
        with self.assertRaises(NoReverseMatch):
            response = self.client.get(reverse('organisation_detail', kwargs={'organisation_id':str(self.org_1.id)}))

        response = self.client.get(reverse('organisation_detail', kwargs={'pk':str(self.org_1.id)}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'organisation/organisation_detail.html')

        self.client.logout()

        response = self.client.get(reverse('organisation_detail', kwargs={'pk':str(self.org_1.id)}))
        self.assertRedirects(response, '/user/login/?next=/organisation/detail/'+ str(self.org_1.id) +'/', status_code=302, target_status_code=200, fetch_redirect_response=True)

        logged_in = self.client.login(username='org_1_user_2', password='12345')
        self.assertTrue(logged_in)
        response = self.client.get(reverse('organisation_detail', kwargs={'pk':str(self.org_1.id)}))
        self.assertEqual(response.status_code, 403)
        response = self.client.post(reverse('organisation_detail', kwargs={'pk':str(self.org_1.id)}), data={})
        self.assertEqual(response.status_code, 403)
