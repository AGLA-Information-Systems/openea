import io
import json
import xml.etree.ElementTree as ET
import uuid
from django.test import TestCase
from django.urls import NoReverseMatch, reverse
import openpyxl

from utils.test.helpers import add_object_type_permissions_to_security_group, create_concept, create_model, create_organisation, create_model, create_repository, create_security_group, create_user, create_user_profile
from ontology.models import OModel
from authorization.models import Permission
from organisation.constants import TIME_SCHEDULE_NOW, TIME_SCHEDULE_SCHEDULED


class OModelImportTestCase(TestCase):
    def setUp(self):
        self.org_1 = create_organisation(name='Org 1', description='', location='test')
        self.org_1_user_1 = create_user(username='org_1_user_1')
        self.org_1_user_1_profile = create_user_profile(role='Admin', user=self.org_1_user_1, organisation=self.org_1)
        self.org_1_security_group_1 = create_security_group(name='Org 1 SecG 1', description='', organisation=self.org_1)
        self.org_1_security_group_1.profiles.add(self.org_1_user_1_profile)
        self.object_type = OModel.get_object_type()
        add_object_type_permissions_to_security_group(organisation=self.org_1, security_group=self.org_1_security_group_1, object_type=self.object_type)

        self.org_1_user_2 = create_user(username='org_1_user_2')
        self.org_1_user_2_profile = create_user_profile(role='Admin', user=self.org_1_user_2, organisation=self.org_1)
        self.org_1_security_group_2 = create_security_group(name='Org 1 SecG 2', description='', organisation=self.org_1)
        self.org_1_security_group_2.profiles.add(self.org_1_user_2_profile)

        self.org_1_repo_1 = create_repository(organisation=self.org_1, name='org_1_repo_1')
        self.org_1_model_1 = create_model(repository=self.org_1_repo_1, name='org_1_model_1')
        self.org_1_concept_1 = create_concept(model=self.org_1_model_1, name='org_1_concept_1')

        self.form_data = {
            'model': str(self.org_1_model_1.id),
            'format': '',
            'knowledge_set': 'INSTANCES',
            'time_schedule': '',
            'concepts': 'true',
            'relations': 'true',
            'predicates': 'true',
            'instances': 'true',
        }

        self.json_data = json.loads("""{
            "id": "",
            "type": "model",
            "name": "",
            "version": "1.0",
            "description": "",
            "concepts": {},
            "relations": {},
            "predicates": {},
            "instances": {
                "5f359074-8129-4719-8d9b-42bfba6c4555": {
                    "id": "5f359074-8129-4719-8d9b-42bfba6c4555",
                    "name": "inst11",
                    "code": "",
                    "description": "",
                    "concept_id": "",
                    "concept": "",
                    "ownslots": {},
                    "inslots": {},
                    "url": "/o_instance/detail/5f359074-8129-4719-8d9b-42bfba6c4555"
                },
                "872d4e2b-2c98-4c54-9e59-d05dff914262": {
                    "id": "872d4e2b-2c98-4c54-9e59-d05dff914262",
                    "name": "inst12",
                    "code": "",
                    "description": "",
                    "concept_id": "",
                    "concept": "",
                    "ownslots": {},
                    "inslots": {},
                    "url": "/o_instance/detail/872d4e2b-2c98-4c54-9e59-d05dff914262"
                }
            },
            "url": "/o_model/detail/075ba23e-314e-4cb9-b5b2-354858348ace"
        }
        """)

        self.xml_data = """<?xml version="1.0" encoding="utf-8"?>
        <model>
            <id></id>
            <type>model</type>
            <name></name>
            <version>1.0</version>
            <description></description>
            <concepts></concepts>
            <relations></relations>
            <predicates></predicates>
            <instances>
                <instance>
                    <id>5f359074-8129-4719-8d9b-42bfba6c4555</id>
                    <name>inst11</name>
                    <code></code>
                    <description></description>
                    <concept_id></concept_id>
                    <concept></concept>
                    <ownslots>
                    </ownslots>
                    <inslots>
                    </inslots>
                    <url>/o_instance/detail/5f359074-8129-4719-8d9b-42bfba6c4555</url>
                </instance>
                <instance>
                    <id>872d4e2b-2c98-4c54-9e59-d05dff914262</id>
                    <name>inst12</name>
                    <code></code>
                    <description></description>
                    <concept_id></concept_id>
                    <concept></concept>
                    <ownslots>
                    </ownslots>
                    <inslots>
                    </inslots>
                    <url>/o_instance/detail/872d4e2b-2c98-4c54-9e59-d05dff914262</url>
                </instance>
            </instances>
        </model>
    """

    def test_o_model_import_page_not_authenticated(self):
        with self.assertRaises(NoReverseMatch):
            response = self.client.get(reverse('o_model_import'))

        bogus_uuid = uuid.uuid4()
        response = self.client.get(reverse('o_model_import', kwargs={'model_id': bogus_uuid}))
        self.assertRedirects(response, '/user/login/?redirect_to=/o_model/'+ str(bogus_uuid) +'/import', status_code=302, target_status_code=200, fetch_redirect_response=True)
        response = self.client.get(reverse('o_model_import', kwargs={'model_id': self.org_1_model_1.id}))
        self.assertRedirects(response, '/user/login/?redirect_to=/o_model/' + str(self.org_1_model_1.id) +'/import', status_code=302, target_status_code=200, fetch_redirect_response=True)
        response = self.client.post(reverse('o_model_import', kwargs={'model_id': self.org_1_model_1.id}), data={})
        self.assertRedirects(response, '/user/login/?redirect_to=/o_model/' + str(self.org_1_model_1.id) +'/import', status_code=302, target_status_code=200, fetch_redirect_response=True)
            
    def test_o_model_import_page_authenticated_not_allowed(self):
        bogus_uuid = uuid.uuid4()
        logged_in = self.client.login(username='org_1_user_1', password='12345')
        self.assertTrue(logged_in)
        response = self.client.get(reverse('o_model_import', kwargs={'model_id': bogus_uuid}))
        self.assertEqual(response.status_code, 403)
        response = self.client.post(reverse('o_model_import', kwargs={'model_id': bogus_uuid}), data={})
        self.assertEqual(response.status_code, 403)
        response = self.client.get(reverse('o_model_import', kwargs={'model_id': self.org_1_model_1.id}))
        self.assertEqual(response.status_code, 403)
        response = self.client.post(reverse('o_model_import', kwargs={'model_id': self.org_1_model_1.id}), data={})
        self.assertEqual(response.status_code, 403)

    def test_o_model_json_import(self):
        # login as org_1_user_1 and activate org_1_user_1_profile
        logged_in = self.client.login(username='org_1_user_1', password='12345')
        self.assertTrue(logged_in)
        self.assertTrue(self.org_1_user_1.profiles.filter(id=self.org_1_user_1_profile.id).exists())
        self.assertTrue(not hasattr(self.org_1_user_1, 'active_profile'))
        response = self.client.post(reverse('profile_activate', kwargs={'pk':str(self.org_1_user_1_profile.id)}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.org_1_user_1_profile.organisation == self.org_1)
        self.assertTrue(self.org_1_user_1_profile.security_groups.filter(id=self.org_1_security_group_1.id).exists())

        # check if the required permission is in the security group
        required_permission = Permission.objects.get(organisation=self.org_1, action='IMPORT', object_type=self.object_type)
        self.assertIsNotNone(required_permission)
        self.assertTrue(self.org_1_security_group_1.permissions.filter(id=required_permission.id).exists())

        with self.assertRaises(NoReverseMatch):
            response = self.client.get(reverse('o_model_import'))
        with self.assertRaises(NoReverseMatch):
            response = self.client.get(reverse('o_model_import', kwargs={'o_model_id':str(self.org_1_model_1.id)}))

        # check if the proper template is used
        response = self.client.get(reverse('o_model_import', kwargs={'model_id':str(self.org_1_model_1.id)}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'o_model/o_model_import.html')

        self.json_data['id'] = str(self.org_1_model_1.id)
        self.json_data['name'] = self.org_1_model_1.name
        
        for instance in self.json_data['instances']:
            self.json_data['instances'][instance]['concept_id'] = str(self.org_1_concept_1.id)
            self.json_data['instances'][instance]['concept'] = self.org_1_concept_1.name

        file_content = json.dumps(self.json_data, indent=4).encode('utf-8')
        file = io.BytesIO(file_content)
        file.name = 'import_file.json'
        file.content_type = 'application/json'

        # update the form data
        self.form_data['format'] = 'JSON'
        self.form_data['import_file'] = file

        # test import with TIME_SCHEDULE_NOW
        self.form_data['time_schedule'] = TIME_SCHEDULE_NOW
        response = self.client.post(reverse('o_model_import', kwargs={'model_id':str(self.org_1_model_1.id)}), data=self.form_data, format='multipart')
        self.assertEqual(response.status_code, 302)

        # test import with TIME_SCHEDULE_SCHEDULED
        self.form_data['time_schedule'] = TIME_SCHEDULE_SCHEDULED
        response = self.client.post(reverse('o_model_import', kwargs={'model_id':str(self.org_1_model_1.id)}), data=self.form_data, format='multipart')
        self.assertEqual(response.status_code, 200)

        self.client.logout()

        response = self.client.get(reverse('o_model_export', kwargs={'model_id': self.org_1_model_1.id}))
        self.assertRedirects(response, '/user/login/?redirect_to=/o_model/' + str(self.org_1_model_1.id) +'/export', status_code=302, target_status_code=200, fetch_redirect_response=True)

    """def test_o_model_xml_import(self):
        # login as org_1_user_1 and activate org_1_user_1_profile
        logged_in = self.client.login(username='org_1_user_1', password='12345')
        self.assertTrue(logged_in)
        self.assertTrue(self.org_1_user_1.profiles.filter(id=self.org_1_user_1_profile.id).exists())
        self.assertTrue(not hasattr(self.org_1_user_1, 'active_profile'))
        response = self.client.post(reverse('profile_activate', kwargs={'pk':str(self.org_1_user_1_profile.id)}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.org_1_user_1_profile.organisation == self.org_1)
        self.assertTrue(self.org_1_user_1_profile.security_groups.filter(id=self.org_1_security_group_1.id).exists())

        # check if the required permission is in the security group
        required_permission = Permission.objects.get(organisation=self.org_1, action='IMPORT', object_type=self.object_type)
        self.assertIsNotNone(required_permission)
        self.assertTrue(self.org_1_security_group_1.permissions.filter(id=required_permission.id).exists())

        with self.assertRaises(NoReverseMatch):
            response = self.client.get(reverse('o_model_import'))
        with self.assertRaises(NoReverseMatch):
            response = self.client.get(reverse('o_model_import', kwargs={'o_model_id':str(self.org_1_model_1.id)}))

        # check if the proper template is used
        response = self.client.get(reverse('o_model_import', kwargs={'model_id':str(self.org_1_model_1.id)}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'o_model/o_model_import.html')

        # Parse the XML data and replace the ids and names with the ones from the test data
        xml_root = ET.fromstring(self.xml_data)
        instances = xml_root.findall('.//instance')

        xml_root_id = xml_root.find('id')
        xml_root_id.text = str(self.org_1_model_1.id)
        xml_root_name = xml_root.find('name')
        xml_root_name.text = self.org_1_model_1.name

        for instance in instances:
            id_element = instance.find('concept_id')
            id_element.text = str(self.org_1_concept_1.id)

            name_element = instance.find('name')
            name_element.text = self.org_1_concept_1.name

        # Create a file-like object from the XML data
        file_content = ET.tostring(xml_root, encoding='utf-8', method='xml')

        file = io.BytesIO(file_content)
        file.name = 'import_file.xml'
        file.content_type = 'application/xml'

        # update the form data
        self.form_data['format'] = 'XML'
        self.form_data['import_file'] = file

        # test import with TIME_SCHEDULE_NOW
        self.form_data['time_schedule'] = TIME_SCHEDULE_NOW
        response = self.client.post(reverse('o_model_import', kwargs={'model_id':str(self.org_1_model_1.id)}), data=self.form_data, format='multipart')
        self.assertEqual(response.status_code, 302) 

        # test import with TIME_SCHEDULE_SCHEDULED
        self.form_data['time_schedule'] = TIME_SCHEDULE_SCHEDULED
        response = self.client.post(reverse('o_model_import', kwargs={'model_id':str(self.org_1_model_1.id)}), data=self.form_data, format='multipart')
        self.assertEqual(response.status_code, 200)

        self.client.logout()

        response = self.client.get(reverse('o_model_export', kwargs={'model_id': self.org_1_model_1.id}))
        self.assertRedirects(response, '/user/login/?redirect_to=/o_model/' + str(self.org_1_model_1.id) +'/export', status_code=302, target_status_code=200, fetch_redirect_response=True)
"""

    def test_o_model_excel_import(self):
        # login as org_1_user_1 and activate org_1_user_1_profile
        logged_in = self.client.login(username='org_1_user_1', password='12345')
        self.assertTrue(logged_in)
        self.assertTrue(self.org_1_user_1.profiles.filter(id=self.org_1_user_1_profile.id).exists())
        self.assertTrue(not hasattr(self.org_1_user_1, 'active_profile'))
        response = self.client.post(reverse('profile_activate', kwargs={'pk':str(self.org_1_user_1_profile.id)}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.org_1_user_1_profile.organisation == self.org_1)
        self.assertTrue(self.org_1_user_1_profile.security_groups.filter(id=self.org_1_security_group_1.id).exists())

        # check if the required permission is in the security group
        required_permission = Permission.objects.get(organisation=self.org_1, action='IMPORT', object_type=self.object_type)
        self.assertIsNotNone(required_permission)
        self.assertTrue(self.org_1_security_group_1.permissions.filter(id=required_permission.id).exists())

        with self.assertRaises(NoReverseMatch):
            response = self.client.get(reverse('o_model_import'))
        with self.assertRaises(NoReverseMatch):
            response = self.client.get(reverse('o_model_import', kwargs={'o_model_id':str(self.org_1_model_1.id)}))

        # check if the proper template is used
        response = self.client.get(reverse('o_model_import', kwargs={'model_id':str(self.org_1_model_1.id)}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'o_model/o_model_import.html')

        # Create an excel file
        workbook = openpyxl.Workbook()
        sheet_names = ['instances']
        for sheet_name in sheet_names:
            workbook.create_sheet(sheet_name)

        sheet = workbook['instances']

        sheet.append(['InstanceID', 'Instance', 'Instance Code', 'Description',
                      'ConceptID', 'Concept',
                      'SlotID', 'Slot' , 'Slot Order', 'Slot Description',
                      'PredicateID', 'Cardinality Min', 'Cardinality Max',
                      'RelationID', 'Relation',
                      'Object ConceptID', 'Object Concept',
                      'ObjectID', 'Object', 'Object Code', 'Object Description'])
        
        sheet.column_dimensions['A'].hidden = True
        sheet.column_dimensions['B'].width = 25
        sheet.column_dimensions['C'].width = 10
        sheet.column_dimensions['D'].hidden = True

        sheet.column_dimensions['E'].hidden = True
        sheet.column_dimensions['F'].width = 25

        sheet.column_dimensions['G'].hidden = True
        sheet.column_dimensions['H'].width = 25
        sheet.column_dimensions['I'].width = 25
        sheet.column_dimensions['J'].hidden = True

        sheet.column_dimensions['K'].hidden = True
        sheet.column_dimensions['L'].width = 10
        sheet.column_dimensions['M'].width = 10

        sheet.column_dimensions['N'].hidden = True
        sheet.column_dimensions['O'].width = 25

        sheet.column_dimensions['P'].hidden = True
        sheet.column_dimensions['Q'].width = 25

        sheet.column_dimensions['R'].hidden = True
        sheet.column_dimensions['S'].width = 25
        sheet.column_dimensions['T'].width = 10
        sheet.column_dimensions['U'].hidden = True

        for instance in self.json_data['instances']:
            for slot in self.json_data['instances'][instance]['ownslots']:
                row = [
                    instance['id'],
                    instance['name'],
                    instance['code'],
                    instance['description'],
                    instance['concept_id'],
                    instance['concept_name'],
                    slot['id'],
                    slot['name'],
                    slot['order'],
                    slot['description'],
                    slot['predicate_id'],
                    slot['cardinality_min'],
                    slot['cardinality_max'],
                    slot['relation_id'],
                    slot['relation_name'],
                    slot['object_concept_id'],
                    slot['object_concept_name'],
                    slot['object_id'],
                    slot['object_name'],
                    slot['object_code'],
                    slot['object_description']
                ]
                sheet.append(row)

        file = io.BytesIO()
        workbook.save(file)
        file.seek(0)
        file.name = 'import_file.xlsx'
        file.content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

        # update the form data
        self.form_data['format'] = 'EXCEL'
        self.form_data['import_file'] = file

        # test import with TIME_SCHEDULE_NOW
        self.form_data['time_schedule'] = TIME_SCHEDULE_NOW
        response = self.client.post(reverse('o_model_import', kwargs={'model_id':str(self.org_1_model_1.id)}), data=self.form_data, format='multipart')
        self.assertEqual(response.status_code, 302)

        # test import with TIME_SCHEDULE_SCHEDULED
        self.form_data['time_schedule'] = TIME_SCHEDULE_SCHEDULED
        response = self.client.post(reverse('o_model_import', kwargs={'model_id':str(self.org_1_model_1.id)}), data=self.form_data, format='multipart')
        self.assertEqual(response.status_code, 200)

        self.client.logout()

        response = self.client.get(reverse('o_model_export', kwargs={'model_id': self.org_1_model_1.id}))
        self.assertRedirects(response, '/user/login/?redirect_to=/o_model/' + str(self.org_1_model_1.id) +'/export', status_code=302, target_status_code=200, fetch_redirect_response=True)