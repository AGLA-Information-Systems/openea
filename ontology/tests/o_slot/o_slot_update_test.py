import uuid
from django.test import TestCase
from django.urls import NoReverseMatch, reverse
from ontology.models import QUALITY_STATUS_PROPOSED, OSlot
from utils.test.helpers import add_object_type_accesspermissions_to_security_group, create_accesspermission, create_concept, create_instance, create_model, create_organisation, create_relation, create_slot, create_predicate, create_repository, create_security_group, create_user, create_user_profile

from authorization.models import Permission


class OSlotUpdateTestCase(TestCase):
    def setUp(self):
        self.org_1 = create_organisation(name='Org 1', description='', location='test')
        self.org_1_user_1 = create_user(username='org_1_user_1')
        self.org_1_user_1_profile = create_user_profile(role='Admin', user=self.org_1_user_1, organisation=self.org_1)
        self.org_1_security_group_1 = create_security_group(name='Org 1 SecG 1', description='', organisation=self.org_1)
        self.org_1_security_group_1.profiles.add(self.org_1_user_1_profile)
        self.object_type = OSlot.get_object_type()
        add_object_type_accesspermissions_to_security_group(organisation=self.org_1, security_group=self.org_1_security_group_1, object_type=self.object_type)

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

        self.org_1_concept_3 = create_concept(model=self.org_1_model_1, name='org_1_concept_3')
        self.org_1_concept_4 = create_concept(model=self.org_1_model_1, name='org_1_concept_4')
        self.org_1_predicate_2 = create_predicate(model=self.org_1_model_1, subject=self.org_1_concept_3, relation=self.org_1_relation_1, object=self.org_1_concept_4)
        self.org_1_instance_3 = create_instance(model=self.org_1_model_1, concept=self.org_1_concept_3, name='org_1_instance_3')
        self.org_1_instance_4 = create_instance(model=self.org_1_model_1, concept=self.org_1_concept_4, name='org_1_instance_4')
        self.model_1_slot_2 = create_slot(model=self.org_1_model_1, subject=self.org_1_instance_3, predicate=self.org_1_predicate_2, object=self.org_1_instance_4)

        self.org_1_instance_5 = create_instance(model=self.org_1_model_1, concept=self.org_1_concept_2, name='org_1_instance_5')
        
    def test_o_slot_update_page_not_authenticated(self):
        with self.assertRaises(NoReverseMatch):
            response = self.client.get(reverse('o_slot_update'))
        bogus_uuid = uuid.uuid4()
        response = self.client.get(reverse('o_slot_update', kwargs={'pk': bogus_uuid}))
        self.assertRedirects(response, '/user/login/?next=/o_slot/update/'+ str(bogus_uuid) +'/', status_code=302, target_status_code=200, fetch_redirect_response=True)
        response = self.client.get(reverse('o_slot_update', kwargs={'pk': self.model_1_slot_1.id}))
        self.assertRedirects(response, '/user/login/?next=/o_slot/update/' + str(self.model_1_slot_1.id) +'/', status_code=302, target_status_code=200, fetch_redirect_response=True)
        response = self.client.post(reverse('o_slot_update', kwargs={'pk': self.model_1_slot_1.id}), data={})
        self.assertRedirects(response, '/user/login/?next=/o_slot/update/' + str(self.model_1_slot_1.id) +'/', status_code=302, target_status_code=200, fetch_redirect_response=True)
        
    def test_o_slot_update_page_authenticated_not_allowed(self):
        bogus_uuid = uuid.uuid4()
        logged_in = self.client.login(username='org_1_user_1', password='12345')
        self.assertTrue(logged_in)
        response = self.client.get(reverse('o_slot_update', kwargs={'pk': bogus_uuid}))
        self.assertEqual(response.status_code, 403)
        response = self.client.post(reverse('o_slot_update', kwargs={'pk': bogus_uuid}), data={})
        self.assertEqual(response.status_code, 403)
        response = self.client.get(reverse('o_slot_update', kwargs={'pk': self.model_1_slot_1.id}))
        self.assertEqual(response.status_code, 403)
        response = self.client.post(reverse('o_slot_update', kwargs={'pk': self.model_1_slot_1.id}), data={})
        self.assertEqual(response.status_code, 403)

    def test_o_slot_update_page_success(self):
        logged_in = self.client.login(username='org_1_user_1', password='12345')
        self.assertTrue(logged_in)
        self.assertTrue(self.org_1_user_1.profiles.filter(id=self.org_1_user_1_profile.id).exists())
        self.assertTrue(not hasattr(self.org_1_user_1, 'active_profile'))
        response = self.client.post(reverse('profile_activate', kwargs={'pk':str(self.org_1_user_1_profile.id)}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.org_1_user_1_profile.organisation == self.org_1)
        self.assertTrue(self.org_1_user_1_profile.security_groups.filter(id=self.org_1_security_group_1.id).exists())
        
        create_accesspermission(security_group=self.org_1_security_group_1, action='UPDATE', object_type=self.object_type)

        with self.assertRaises(NoReverseMatch):
            response = self.client.get(reverse('o_slot_update'))
        with self.assertRaises(NoReverseMatch):
            response = self.client.get(reverse('o_slot_update', kwargs={'o_slot_id':str(self.model_1_slot_1.id)}))

        response = self.client.get(reverse('o_slot_update', kwargs={'pk':str(self.model_1_slot_1.id)}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'o_slot/o_slot_update.html')
        response = self.client.post(reverse('o_slot_update', kwargs={'pk':str(self.model_1_slot_1.id)}), data={'name':'Slot 1', 'description': ''})
        self.assertEqual(response.status_code, 200) #TODO : Not 200 in case of error
        response = self.client.post(reverse('o_slot_update', kwargs={'pk':str(self.model_1_slot_1.id)}),
                                    data={'subject': self.org_1_instance_3.id,
                                        'predicate':self.org_1_predicate_2.id,
                                        'object':self.org_1_instance_4.id,
                                        'model':self.org_1_model_1.id})
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('o_slot_update', kwargs={'pk':str(self.model_1_slot_1.id)}),
                                    data={'subject': self.org_1_instance_1.id,
                                        'predicate':self.org_1_predicate_1.id,
                                        'object':self.org_1_instance_5.id,
                                        'order': '1.1',
                                        'model':self.org_1_model_1.id})
        self.assertEqual(response.status_code, 302, response.content) #response.context["form"].errors

        updated_o_slot = OSlot.objects.get(id=self.model_1_slot_1.id)
        self.assertEqual(updated_o_slot.subject, self.org_1_instance_1)
        self.assertEqual(updated_o_slot.predicate, self.org_1_predicate_1)
        self.assertEqual(updated_o_slot.object, self.org_1_instance_5)

        self.client.logout()

        response = self.client.get(reverse('o_slot_update', kwargs={'pk':str(self.model_1_slot_1.id)}))
        self.assertRedirects(response, '/user/login/?next=/o_slot/update/'+ str(self.model_1_slot_1.id) +'/', status_code=302, target_status_code=200, fetch_redirect_response=True)

        logged_in = self.client.login(username='org_1_user_2', password='12345')
        self.assertTrue(logged_in)
        response = self.client.get(reverse('o_slot_update', kwargs={'pk':str(self.model_1_slot_1.id)}))
        self.assertEqual(response.status_code, 403)
        response = self.client.post(reverse('o_slot_update', kwargs={'pk':str(self.model_1_slot_1.id)}), data={})
        self.assertEqual(response.status_code, 403)
