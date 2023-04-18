import uuid

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import NoReverseMatch, reverse

from authorization.models import Permission
from utils.test.helpers import (add_object_type_permissions_to_security_group,
                                create_organisation, create_security_group,
                                create_task, create_user, create_user_profile)
from organisation.models import Task


class TaskUpdateTestCase(TestCase):
    def setUp(self):
        self.org_1 = create_organisation(name='Org 1', description='', location='test')
        self.org_1_user_1 = create_user(username='org_1_user_1')
        self.org_1_user_1_profile = create_user_profile(role='Admin', user=self.org_1_user_1, organisation=self.org_1)
        self.org_1_security_group_1 = create_security_group(name='Org 1 SecG 1', description='', organisation=self.org_1)
        self.org_1_security_group_1.profiles.add(self.org_1_user_1_profile)
        self.object_type = Task.get_object_type()
        add_object_type_permissions_to_security_group(organisation=self.org_1, security_group=self.org_1_security_group_1, object_type=self.object_type)

        self.org_1_user_2 = create_user(username='org_1_user_2')
        self.org_1_user_2_profile = create_user_profile(role='Admin', user=self.org_1_user_2, organisation=self.org_1)
        self.org_1_security_group_2 = create_security_group(name='Org 1 SecG 2', description='', organisation=self.org_1)
        self.org_1_security_group_2.profiles.add(self.org_1_user_2_profile)

        self.org_1_task_1 = create_task(organisation=self.org_1, user=self.org_1_user_1, name='Org 1 Task 1')
        
    def test_task_update_page_not_authenticated(self):
        with self.assertRaises(NoReverseMatch):
            response = self.client.get(reverse('task_update'))
        bogus_uuid = uuid.uuid4()
        response = self.client.get(reverse('task_update', kwargs={'pk': bogus_uuid}))
        self.assertRedirects(response, '/user/login/?redirect_to=/task/update/'+ str(bogus_uuid) +'/', status_code=302, target_status_code=200, fetch_redirect_response=True)
        response = self.client.get(reverse('task_update', kwargs={'pk': self.org_1_task_1.id}))
        self.assertRedirects(response, '/user/login/?redirect_to=/task/update/' + str(self.org_1_task_1.id) +'/', status_code=302, target_status_code=200, fetch_redirect_response=True)
        response = self.client.post(reverse('task_update', kwargs={'pk': self.org_1_task_1.id}), data={})
        self.assertRedirects(response, '/user/login/?redirect_to=/task/update/' + str(self.org_1_task_1.id) +'/', status_code=302, target_status_code=200, fetch_redirect_response=True)
        
    def test_task_update_page_authenticated_not_allowed(self):
        bogus_uuid = uuid.uuid4()
        logged_in = self.client.login(username='org_1_user_1', password='12345')
        self.assertTrue(logged_in)
        response = self.client.get(reverse('task_update', kwargs={'pk': bogus_uuid}))
        self.assertEqual(response.status_code, 403)
        response = self.client.post(reverse('task_update', kwargs={'pk': bogus_uuid}), data={})
        self.assertEqual(response.status_code, 403)
        response = self.client.get(reverse('task_update', kwargs={'pk': self.org_1_task_1.id}))
        self.assertEqual(response.status_code, 403)
        response = self.client.post(reverse('task_update', kwargs={'pk': self.org_1_task_1.id}), data={})
        self.assertEqual(response.status_code, 403)

    def test_task_update_page_success(self):
        logged_in = self.client.login(username='org_1_user_1', password='12345')
        self.assertTrue(logged_in)
        self.assertTrue(self.org_1_user_1.profiles.filter(id=self.org_1_user_1_profile.id).exists())
        self.assertTrue(not hasattr(self.org_1_user_1, 'active_profile'))
        response = self.client.post(reverse('profile_activate', kwargs={'pk':str(self.org_1_user_1_profile.id)}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.org_1_user_1_profile.organisation == self.org_1)
        self.assertTrue(self.org_1_user_1_profile.security_groups.filter(id=self.org_1_security_group_1.id).exists())
        
        for perm in Permission.objects.filter(organisation=self.org_1, action='UPDATE', object_type=self.object_type):
            print(perm)

        required_permission = Permission.objects.get(organisation=self.org_1, action='UPDATE', object_type=self.object_type)
        self.assertIsNotNone(required_permission)
        perms = [str(x) for x in self.org_1_security_group_1.permissions.all()]
        self.assertTrue(self.org_1_security_group_1.permissions.filter(id=required_permission.id).exists())

        with self.assertRaises(NoReverseMatch):
            response = self.client.get(reverse('task_update'))
        with self.assertRaises(NoReverseMatch):
            response = self.client.get(reverse('task_update', kwargs={'task_id':str(self.org_1_task_1.id)}))

        response = self.client.get(reverse('task_update', kwargs={'pk':str(self.org_1_task_1.id)}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task/task_update.html')
        response = self.client.post(reverse('task_update', kwargs={'pk':str(self.org_1_task_1.id)}), data={'name':'Task 1', 'description': '', 'attachment': ''})
        self.assertEqual(response.status_code, 200) #TODO : Not 200 in case of error

        file_uploaded = SimpleUploadedFile( "best_file_eva.txt", b"these are the file contents!")
        response = self.client.post(reverse('task_update', kwargs={'pk':str(self.org_1_task_1.id)}), data={'name':'Task 1', 'type': 'IMPORT', 'attachment': file_uploaded, 'description': 'Update task', 'organisation':self.org_1.id})
        self.assertEqual(response.status_code, 302, response.content)

        updated_task = Task.objects.get(id=self.org_1_task_1.id)
        self.assertEqual(updated_task.name, 'Task 1')
        self.assertEqual(updated_task.description, 'Update task')

        self.client.logout()

        response = self.client.get(reverse('task_update', kwargs={'pk':str(self.org_1_task_1.id)}))
        self.assertRedirects(response, '/user/login/?redirect_to=/task/update/'+ str(self.org_1_task_1.id) +'/', status_code=302, target_status_code=200, fetch_redirect_response=True)

        logged_in = self.client.login(username='org_1_user_2', password='12345')
        self.assertTrue(logged_in)
        response = self.client.get(reverse('task_update', kwargs={'pk':str(self.org_1_task_1.id)}))
        self.assertEqual(response.status_code, 403)
        response = self.client.post(reverse('task_update', kwargs={'pk':str(self.org_1_task_1.id)}), data={})
        self.assertEqual(response.status_code, 403)