from django.test import TestCase
from django.urls import reverse

from django.contrib.auth.models import User
from authorization.controllers.utils import create_organisation_admin_security_group
from authorization.models import SecurityGroup
from webapp.models import Organisation, Profile

class OrganisationDeleteTestCase(TestCase):
    def setUp(self):
        self.siteadmin_org = Organisation.objects.create(name='Admin Org', description='', location='test')
        self.siteadmin_org.save()
        self.siteadmin_user = User.objects.create(username='orgadminuser')
        self.siteadmin_user.set_password('12345')
        self.siteadmin_user.save()
        self.siteadmin_profile = Profile.objects.create(role='Admin', user=self.siteadmin_user, organisation=self.siteadmin_org, is_active=True)
        self.siteadmin_profile.save()
        self.siteadmin_security_group = create_organisation_admin_security_group(organisation=self.siteadmin_org, admin_security_group_name='Admin Org SecG', superadmin=True)
        self.siteadmin_security_group.profiles.add(self.siteadmin_profile)
        self.siteadmin_security_group.save()


        self.org_1 = Organisation.objects.create(name='Org 1', description='', location='test')
        self.org_1.save()
        self.org_1_admin_user = User.objects.create(username='org1admin')
        self.org_1_admin_user.set_password('12345')
        self.org_1_admin_user.save()
        self.org_1_admin_profile = Profile.objects.create(role='Admin', user=self.org_1_admin_user, organisation=self.org_1, is_active=True)
        self.org_1_admin_profile.save()
        self.org_1_admin_security_group = SecurityGroup.objects.create(name='Org 1 SecG', description='', organisation=self.org_1)
        self.org_1_admin_security_group.profiles.add(self.org_1_admin_profile)

    def test_organisation_delete_page_not_authenticated(self):
        response = self.client.get(reverse('organisation_delete', kwargs={'pk': self.org_1.id}))
        self.assertRedirects(response, '/user/login/?redirect_to=/organisation/delete/{}/'.format(self.org_1.id), status_code=302, target_status_code=200, fetch_redirect_response=True)
        response = self.client.post(reverse('organisation_delete', kwargs={'pk': self.org_1.id}), data={})
        self.assertRedirects(response, '/user/login/?redirect_to=/organisation/delete/{}/'.format(self.org_1.id), status_code=302, target_status_code=200, fetch_redirect_response=True)
        
    def test_organisation_delete_page_authenticated_not_allowed(self):
        logged_in = self.client.login(username='org1admin', password='12345')
        self.assertTrue(logged_in)
        response = self.client.get(reverse('organisation_delete', kwargs={'pk': self.org_1.id}))
        self.assertEqual(response.status_code, 403)
        response = self.client.post(reverse('organisation_delete', kwargs={'pk': self.org_1.id}), data={})
        self.assertEqual(response.status_code, 403)

    def test_organisation_delete_page(self):
        logged_in = self.client.login(username='org1admin', password='12345')
        self.assertTrue(logged_in)
        response = self.client.get(reverse('organisation_delete', kwargs={'pk': self.org_1.id}))
        self.assertEqual(response.status_code, 403)
        self.client.logout()
        logged_in = self.client.login(username='orgadminuser', password='12345')
        self.assertTrue(logged_in)
        response = self.client.get(reverse('organisation_delete', kwargs={'pk': self.org_1.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'organisation/organisation_delete.html')
