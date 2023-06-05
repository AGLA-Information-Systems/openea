import uuid
from django.test import TestCase
from django.urls import reverse
from authorization.models import Permission
from ontology.models import QUALITY_STATUS_PROPOSED, OInstance, OSlot
from utils.test.helpers import add_object_type_permissions_to_security_group, create_instance, create_organisation, create_predicate, create_repository, create_security_group, create_user, create_user_profile, create_model, create_concept, create_relation


class OSlotCreateTestCase(TestCase):
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
        

    def test_o_slot_create_page_not_authenticated(self):
        bogus_uuid = uuid.uuid4()
        response = self.client.get(reverse('o_slot_create', kwargs={'instance_id': bogus_uuid, 'predicate_id': bogus_uuid, 'concept_id': bogus_uuid, 'is_subject': 0}))
        self.assertRedirects(response, '/user/login/?redirect_to=/o_slot/create/'+ str(bogus_uuid) +'/'+ str(bogus_uuid) +'/'+ str(bogus_uuid) +'/0', status_code=302, target_status_code=200, fetch_redirect_response=True)
        response = self.client.post(reverse('o_slot_create', kwargs={'instance_id': bogus_uuid, 'predicate_id': bogus_uuid, 'concept_id': bogus_uuid, 'is_subject': 0}), data={})
        self.assertRedirects(response, '/user/login/?redirect_to=/o_slot/create/'+ str(bogus_uuid) +'/'+ str(bogus_uuid) +'/'+ str(bogus_uuid) +'/0', status_code=302, target_status_code=200, fetch_redirect_response=True)
        
    def test_o_slot_create_page_authenticated_not_allowed(self):
        bogus_uuid = uuid.uuid4()
        logged_in = self.client.login(username='org_1_user_1', password='12345')
        self.assertTrue(logged_in)
        response = self.client.get(reverse('o_slot_create', kwargs={'instance_id': bogus_uuid, 'predicate_id': bogus_uuid, 'concept_id': bogus_uuid, 'is_subject': 0}))
        self.assertEqual(response.status_code, 403)
        response = self.client.post(reverse('o_slot_create', kwargs={'instance_id': bogus_uuid, 'predicate_id': bogus_uuid, 'concept_id': bogus_uuid, 'is_subject': 0}), data={})
        self.assertEqual(response.status_code, 403)

        response = self.client.get(reverse('o_slot_create', kwargs={'instance_id': self.org_1_instance_1.id, 'predicate_id': self.org_1_predicate_1.id, 'concept_id': self.org_1_concept_2.id, 'is_subject': 0}))
        self.assertEqual(response.status_code, 403)
        response = self.client.post(reverse('o_slot_create', kwargs={'instance_id': self.org_1_instance_1.id, 'predicate_id': self.org_1_predicate_1.id, 'concept_id': self.org_1_concept_2.id, 'is_subject': 0}), data={})
        self.assertEqual(response.status_code, 403)

    def test_o_slot_create_page_success(self):
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


        response = self.client.get(reverse('o_slot_create', kwargs={'instance_id': self.org_1_instance_1.id, 'predicate_id': self.org_1_predicate_1.id, 'concept_id': self.org_1_concept_2.id, 'is_subject': 0}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'o_slot/o_slot_create.html')
        response = self.client.post(reverse('o_slot_create', kwargs={'instance_id': self.org_1_instance_1.id, 'predicate_id': self.org_1_predicate_1.id, 'concept_id': self.org_1_concept_2.id, 'is_subject': 0}),
                                                             data={'name':'Slot 1', 'description': ''})
        self.assertEqual(response.status_code, 200) #TODO : Not 200 in case of error
        
        response = self.client.post(reverse('o_slot_create', kwargs={'instance_id': self.org_1_instance_1.id, 'predicate_id': self.org_1_predicate_1.id, 'concept_id': self.org_1_concept_2.id, 'is_subject': 0}), 
                                    data={'subject': self.org_1_instance_1.id,
                                          'object': self.org_1_instance_2.id,
                                          'order': '1.1',
                                          'model': self.org_1_model_1.id})
        self.assertEqual(response.status_code, 302, response.content)
        slot = OSlot.objects.get(predicate=self.org_1_predicate_1, subject=self.org_1_instance_1, object=self.org_1_instance_2)

        response = self.client.post(reverse('o_slot_create', kwargs={'instance_id': self.org_1_instance_1.id, 'predicate_id': self.org_1_predicate_1.id, 'concept_id': self.org_1_concept_2.id, 'is_subject': 1}), 
                                    data={'subject': self.org_1_instance_1.id,
                                          'object': '',
                                          'new_object_name': 'org_1_instance_3',
                                          'new_object_description': '',
                                          'order': '1.1',
                                          'model': self.org_1_model_1.id})
        self.assertEqual(response.status_code, 302, response.content)
        instance_3 = OInstance.objects.get(name='org_1_instance_3')
        slot = OSlot.objects.get(predicate=self.org_1_predicate_1, subject=self.org_1_instance_1, object=instance_3)

        response = self.client.post(reverse('o_slot_create', kwargs={'instance_id': self.org_1_instance_2.id, 'predicate_id': self.org_1_predicate_1.id, 'concept_id': self.org_1_concept_1.id, 'is_subject': 0}), 
                                    data={'subject': '',
                                          'object': self.org_1_instance_2.id,
                                          'new_object_name': 'org_1_instance_4',
                                          'new_object_description': '',
                                          'order': '1.1',
                                          'model': self.org_1_model_1.id})
        self.assertEqual(response.status_code, 302, response.content)
        instance_4 = OInstance.objects.get(name='org_1_instance_4')
        slot = OSlot.objects.get(predicate=self.org_1_predicate_1, subject=instance_4, object=self.org_1_instance_2)

        self.client.logout()

        response = self.client.get(reverse('o_slot_create', kwargs={'instance_id': self.org_1_instance_1.id, 'predicate_id': self.org_1_predicate_1.id, 'concept_id': self.org_1_concept_2.id, 'is_subject': 0}))
        self.assertRedirects(response, '/user/login/?redirect_to=/o_slot/create/'+ str(self.org_1_instance_1.id) +'/'+ str(self.org_1_predicate_1.id) +'/'+ str(self.org_1_concept_2.id) +'/0', status_code=302, target_status_code=200, fetch_redirect_response=True)

        logged_in = self.client.login(username='org_1_user_2', password='12345')
        self.assertTrue(logged_in)
        response = self.client.get(reverse('o_slot_create', kwargs={'instance_id': self.org_1_instance_1.id, 'predicate_id': self.org_1_predicate_1.id, 'concept_id': self.org_1_concept_2.id, 'is_subject': 0}))
        self.assertEqual(response.status_code, 403)
        response = self.client.post(reverse('o_slot_create', kwargs={'instance_id': self.org_1_instance_1.id, 'predicate_id': self.org_1_predicate_1.id, 'concept_id': self.org_1_concept_2.id, 'is_subject': 0}), data={})
        self.assertEqual(response.status_code, 403)
