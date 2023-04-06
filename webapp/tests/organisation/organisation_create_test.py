from pydoc import describe
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from authorization.controllers.utils import create_organisation_admin_security_group
from authorization.models import Permission, SecurityGroup
from webapp.models import Organisation, Profile
from utils.test.helpers import create_organisation, create_security_group, create_user, create_user_profile

class OrganisationCreateTestCase(TestCase):
    def setUp(self):
        self.siteadmin_org = Organisation.objects.create(name='Admin Org', description='', location='test')
        self.siteadmin_org.save()
        self.siteadmin_user = User.objects.create(username='orgadminuser')
        self.siteadmin_user.set_password('12345')
        self.siteadmin_user.save()
        self.siteadmin_profile = Profile.objects.create(role='Admin', user=self.siteadmin_user, organisation=self.siteadmin_org)
        self.siteadmin_profile.save()
        self.siteadmin_security_group = create_organisation_admin_security_group(organisation=self.siteadmin_org, admin_security_group_name='Admin Org SecG', superadmin=True)
        self.siteadmin_security_group.profiles.add(self.siteadmin_profile)
        self.siteadmin_security_group.save()


        self.org_1 = create_organisation(name='Org 1', description='', location='test')
        self.org_1_admin_user = create_user(username='org1admin')
        self.org_1_admin_profile = create_user_profile(role='Admin', user=self.siteadmin_user, organisation=self.org_1)
        self.org_1_admin_security_group = create_security_group(name='Org 1 SecG', description='', organisation=self.org_1)
        self.org_1_admin_security_group.profiles.add(self.org_1_admin_profile)


    def test_organisation_create_page_not_authenticated(self):
        response = self.client.get(reverse('organisation_create'))
        self.assertRedirects(response, '/user/login/?redirect_to=/organisation/create/', status_code=302, target_status_code=200, fetch_redirect_response=True)
        response = self.client.post(reverse('organisation_create'), data={})
        self.assertRedirects(response, '/user/login/?redirect_to=/organisation/create/', status_code=302, target_status_code=200, fetch_redirect_response=True)
        
    def test_organisation_create_page_authenticated_not_allowed(self):
        logged_in = self.client.login(username='org1admin', password='12345')
        self.assertTrue(logged_in)
        response = self.client.get(reverse('organisation_create'))
        self.assertEqual(response.status_code, 403)
        response = self.client.post(reverse('organisation_create'), data={})
        self.assertEqual(response.status_code, 403)

    def test_organisation_create_page_success(self):
        logged_in = self.client.login(username='orgadminuser', password='12345')
        self.assertTrue(logged_in)
        self.assertTrue(self.siteadmin_user.profiles.filter(id=self.siteadmin_profile.id).exists())
        self.assertTrue(not hasattr(self.siteadmin_user, 'active_profile'))
        response = self.client.post(reverse('profile_activate', kwargs={'pk':str(self.siteadmin_profile.id)}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.siteadmin_profile.organisation == self.siteadmin_org)
        self.assertTrue(self.siteadmin_profile.security_groups.filter(id=self.siteadmin_security_group.id).exists())
        
        required_permission = Permission.objects.get(organisation=self.siteadmin_org, action='CREATE', object_type=self.siteadmin_org.__class__.get_object_type())
        self.assertIsNotNone(required_permission)
        perms = [str(x) for x in self.siteadmin_security_group.permissions.all()]
        self.assertTrue(self.siteadmin_security_group.permissions.filter(id=required_permission.id).exists())

        response = self.client.get(reverse('organisation_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'organisation/organisation_create.html')
        response = self.client.post(reverse('organisation_create'), data={'name':'Org 2', 'description': '', 'location': 'test'})
        self.assertEqual(response.status_code, 302)

        self.client.logout()

        response = self.client.get(reverse('organisation_create'))
        self.assertRedirects(response, '/user/login/?redirect_to=/organisation/create/', status_code=302, target_status_code=200, fetch_redirect_response=True)
