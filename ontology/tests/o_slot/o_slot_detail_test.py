import uuid
from django.test import TestCase
from django.urls import NoReverseMatch, reverse
from ontology.models import QUALITY_STATUS_PROPOSED, OSlot
from utils.test.helpers import add_object_type_permissions_to_security_group, create_concept, create_instance, create_model, create_organisation, create_relation, create_slot, create_predicate, create_repository, create_security_group, create_user, create_user_profile

from authorization.models import Permission


class OSlotDetailTestCase(TestCase):
    def setUp(self):
        self.org_1 = create_organisation(name='Org 1', description='', location='test')
        self.org_1_user_1 = create_user(username='org_1_user_1')
        self.org_1_user_1_profile = create_user_profile(role='Admin', user=self.org_1_user_1, organisation=self.org_1)
        self.org_1_security_group_1 = create_security_group(name='Org 1 SecG 1', description='', organisation=self.org_1)
        self.org_1_security_group_1.profiles.add(self.org_1_user_1_profile)
        self.object_type = OSlot.get_object_type()
        add_object_type_permissions_to_security_group(organisation=self.org_1, security_group=self.org_1_security_group_1, object_type=self.object_type)

        self.org_1_user_2 = create_user(username='org_1_user_2')
        self.org_1_user_2_profile = create_user_profile(role='Admin', user=self.org_1_user_2, organisation=self.org_1)
        self.org_1_security_group_2 = create_security_group(name='Org 1 SecG 2', description='', organisation=self.org_1)
        self.org_1_security_group_2.profiles.add(self.org_1_user_2_profile)

        self.org_1_repo_1 = create_repository(organisation=self.org_1, name='org_1_repo_1')
        self.org_1_model_1 = create_model(repository=self.org_1_repo_1, name='org_1_model_1')
        self.org_1_relation_1 = create_relation(model=self.org_1_model_1, name='org_1_relation_1')
        self.org_1_concept_1 = create_concept(model=self.org_1_model_1, name='org_1_concept_1')
        self.org_1_concept_2 = create_concept(model=self.org_1_model_1, name='org_1_concept_2')
        self.org_1_predicate_1 = create_predicate(model=self.org_1_model_1, subject=self.org_1_concept_1, relation=self.org_1_relation_1, object=self.org_1_concept_2)
        self.org_1_instance_1 = create_instance(model=self.org_1_model_1, concept=self.org_1_concept_1, name='org_1_instance_1')
        self.org_1_instance_2 = create_instance(model=self.org_1_model_1, concept=self.org_1_concept_2, name='org_1_instance_2')
        self.model_1_slot_1 = create_slot(model=self.org_1_model_1, subject=self.org_1_instance_1, predicate=self.org_1_predicate_1, object=self.org_1_instance_2)
        
    def test_o_slot_detail_page_not_authenticated(self):
        with self.assertRaises(NoReverseMatch):
            response = self.client.get(reverse('o_slot_detail'))
        bogus_uuid = uuid.uuid4()
        response = self.client.get(reverse('o_slot_detail', kwargs={'pk': bogus_uuid}))
        self.assertRedirects(response, '/user/login/?redirect_to=/o_slot/detail/'+ str(bogus_uuid) +'/', status_code=302, target_status_code=200, fetch_redirect_response=True)
        response = self.client.get(reverse('o_slot_detail', kwargs={'pk': self.model_1_slot_1.id}))
        self.assertRedirects(response, '/user/login/?redirect_to=/o_slot/detail/' + str(self.model_1_slot_1.id) +'/', status_code=302, target_status_code=200, fetch_redirect_response=True)
        response = self.client.post(reverse('o_slot_detail', kwargs={'pk': self.model_1_slot_1.id}), data={})
        self.assertRedirects(response, '/user/login/?redirect_to=/o_slot/detail/' + str(self.model_1_slot_1.id) +'/', status_code=302, target_status_code=200, fetch_redirect_response=True)
        
    def test_o_slot_detail_page_authenticated_not_allowed(self):
        bogus_uuid = uuid.uuid4()
        logged_in = self.client.login(username='org_1_user_1', password='12345')
        self.assertTrue(logged_in)
        response = self.client.get(reverse('o_slot_detail', kwargs={'pk': bogus_uuid}))
        self.assertEqual(response.status_code, 403)
        response = self.client.post(reverse('o_slot_detail', kwargs={'pk': bogus_uuid}), data={})
        self.assertEqual(response.status_code, 403)
        response = self.client.get(reverse('o_slot_detail', kwargs={'pk': self.model_1_slot_1.id}))
        self.assertEqual(response.status_code, 403)
        response = self.client.post(reverse('o_slot_detail', kwargs={'pk': self.model_1_slot_1.id}), data={})
        self.assertEqual(response.status_code, 403)

    def test_o_slot_detail_page_success(self):
        logged_in = self.client.login(username='org_1_user_1', password='12345')
        self.assertTrue(logged_in)
        self.assertTrue(self.org_1_user_1.profiles.filter(id=self.org_1_user_1_profile.id).exists())
        self.assertTrue(not hasattr(self.org_1_user_1, 'active_profile'))
        response = self.client.post(reverse('profile_activate', kwargs={'pk':str(self.org_1_user_1_profile.id)}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.org_1_user_1_profile.organisation == self.org_1)
        self.assertTrue(self.org_1_user_1_profile.security_groups.filter(id=self.org_1_security_group_1.id).exists())
        
        for perm in Permission.objects.filter(organisation=self.org_1, action='VIEW', object_type=self.object_type):
            print(perm)

        required_permission = Permission.objects.get(organisation=self.org_1, action='VIEW', object_type=self.object_type)
        self.assertIsNotNone(required_permission)
        perms = [str(x) for x in self.org_1_security_group_1.permissions.all()]
        self.assertTrue(self.org_1_security_group_1.permissions.filter(id=required_permission.id).exists())

        with self.assertRaises(NoReverseMatch):
            response = self.client.get(reverse('o_slot_detail'))
        with self.assertRaises(NoReverseMatch):
            response = self.client.get(reverse('o_slot_detail', kwargs={'o_slot_id':str(self.model_1_slot_1.id)}))

        response = self.client.get(reverse('o_slot_detail', kwargs={'pk':str(self.model_1_slot_1.id)}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'o_slot/o_slot_detail.html')

        self.client.logout()

        response = self.client.get(reverse('o_slot_detail', kwargs={'pk':str(self.model_1_slot_1.id)}))
        self.assertRedirects(response, '/user/login/?redirect_to=/o_slot/detail/'+ str(self.model_1_slot_1.id) +'/', status_code=302, target_status_code=200, fetch_redirect_response=True)

        logged_in = self.client.login(username='org_1_user_2', password='12345')
        self.assertTrue(logged_in)
        response = self.client.get(reverse('o_slot_detail', kwargs={'pk':str(self.model_1_slot_1.id)}))
        self.assertEqual(response.status_code, 403)
        response = self.client.post(reverse('o_slot_detail', kwargs={'pk':str(self.model_1_slot_1.id)}), data={})
        self.assertEqual(response.status_code, 403)
