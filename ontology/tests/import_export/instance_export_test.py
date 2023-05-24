import json
import uuid
from django.test import TestCase
from django.urls import reverse
from authorization.models import Permission
from ontology.models import OInstance, OModel
from ontology.views.import_export import ExportView

from utils.test.helpers import (
    add_object_type_permissions_to_security_group,
    create_concept,
    create_instance,
    create_model,
    create_organisation,
    create_repository,
    create_security_group,
    create_user,
    create_user_profile,
)


class InstanceExportTestCase(TestCase):
    def setUp(self):
        self.org_1 = create_organisation(name="Org 1", description="", location="test")
        self.org_1_user_1 = create_user(username="org_1_user_1")
        self.org_1_user_1_profile = create_user_profile(
            role="Admin", user=self.org_1_user_1, organisation=self.org_1
        )
        self.org_1_security_group_1 = create_security_group(
            name="Org 1 SecG 1", description="", organisation=self.org_1
        )
        self.org_1_security_group_1.profiles.add(self.org_1_user_1_profile)
        self.object_type = OInstance.get_object_type()
        add_object_type_permissions_to_security_group(
            organisation=self.org_1,
            security_group=self.org_1_security_group_1,
            object_type=self.object_type,
        )

        self.org_1_user_2 = create_user(username="org_1_user_2")
        self.org_1_user_2_profile = create_user_profile(
            role="Admin", user=self.org_1_user_2, organisation=self.org_1
        )
        self.org_1_security_group_2 = create_security_group(
            name="Org 1 SecG 2", description="", organisation=self.org_1
        )
        self.org_1_security_group_2.profiles.add(self.org_1_user_2_profile)

        self.org_1_repo_1 = create_repository(
            organisation=self.org_1, name="org_1_repo_1"
        )
        self.org_1_model_1 = create_model(
            repository=self.org_1_repo_1, name="org_1_model_1"
        )
        self.org_1_concept_1 = create_concept(
            model=self.org_1_model_1, name="org_1_concept_1"
        )

        # create some instances
        self.instance_1 = create_instance(
            model=self.org_1_model_1, concept=self.org_1_concept_1, name="instance_1"
        )
        self.instance_2 = create_instance(
            model=self.org_1_model_1, concept=self.org_1_concept_1, name="instance_2"
        )

    def test_export_view_page_not_authenticated(self):
        bogus_uuid = uuid.uuid4()
        response = self.client.get(
            reverse("model_export", kwargs={"model_id": bogus_uuid})
        )
        self.assertRedirects(
            response,
            "/user/login/?redirect_to=/model_export/" + str(bogus_uuid) + "/",
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )
        response = self.client.post(
            reverse("model_export", kwargs={"model_id": bogus_uuid}), data={}
        )
        self.assertRedirects(
            response,
            "/user/login/?redirect_to=/model_export/" + str(bogus_uuid) + "/",
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )

    def test_export_view_page_authenticated_not_allowed(self):
        bogus_uuid = uuid.uuid4()
        logged_in = self.client.login(username="org_1_user_1", password="12345")
        self.assertTrue(logged_in)
        response = self.client.get(
            reverse("model_export", kwargs={"model_id": bogus_uuid})
        )
        self.assertEqual(response.status_code, 403)
        response = self.client.post(
            reverse("model_export", kwargs={"model_id": bogus_uuid}), data={}
        )
        self.assertEqual(response.status_code, 403)

    def test_start_export_view_page_authenticated_success(self):
        # log the user in
        logged_in = self.client.login(username="org_1_user_1", password="12345")
        self.assertTrue(logged_in)
        self.assertTrue(
            self.org_1_user_1.profiles.filter(id=self.org_1_user_1_profile.id).exists()
        )
        self.assertTrue(not hasattr(self.org_1_user_1, "active_profile"))
        response = self.client.post(
            reverse(
                "profile_activate", kwargs={"pk": str(self.org_1_user_1_profile.id)}
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.org_1_user_1_profile.organisation == self.org_1)
        self.assertTrue(
            self.org_1_user_1_profile.security_groups.filter(
                id=self.org_1_security_group_1.id
            ).exists()
        )

        required_permission = Permission.objects.get(
            organisation=self.org_1, action="EXPORT", object_type=self.object_type
        )
        self.assertIsNotNone(required_permission)
        self.assertTrue(
            self.org_1_security_group_1.permissions.filter(
                id=required_permission.id
            ).exists()
        )

        self.org_1_security_group_1.permissions.add(required_permission)

        response = self.client.get(
            reverse("model_export", kwargs={"model_id": self.org_1_model_1.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "model_export.html")
        response = self.client.post(
            reverse("model_export", kwargs={"model_id": self.org_1_model_1.id}),
            data={"export_format": "JSON"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["content-type"], "application/json")
        self.assertEqual(
            response["Content-Disposition"], "attachment; filename=export.json"
        )
        self.assertEqual(
            json.loads(response.content),
            {
                "instances": [
                    {
                        "id": str(self.instance_1.id),
                        "name": "instance_1",
                        "concept": str(self.org_1_concept_1.id),
                        "model": str(self.org_1_model_1.id),
                        "quality": "PROPOSED",
                        "status": "ACTIVE",
                        "properties": [],
                    },
                    {
                        "id": str(self.instance_2.id),
                        "name": "instance_2",
                        "concept": str(self.org_1_concept_1.id),
                        "model": str(self.org_1_model_1.id),
                        "quality": "PROPOSED",
                        "status": "ACTIVE",
                        "properties": [],
                    },
                ]
            },
        )
        response = self.client.post(
            reverse("model_export", kwargs={"model_id": self.org_1_model_1.id}),
            data={
                "export_format": "JSON",
                "selected_instances": [str(self.instance_1.id)],
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["content-type"], "application/json")
        self.assertEqual(
            response["Content-Disposition"], "attachment; filename=export.json"
        )
        self.assertEqual(
            json.loads(response.content),
            {
                "instances": [
                    {
                        "id": str(self.instance_1.id),
                        "name": "instance_1",
                        "concept": str(self.org_1_concept_1.id),
                        "model": str(self.org_1_model_1.id),
                        "quality": "PROPOSED",
                        "status": "ACTIVE",
                        "properties": [],
                    }
                ]
            },
        )

    def test_schedule_export_view_page_authenticated_success(self):
        # log the user in
        logged_in = self.client.login(username="org_1_user_1", password="12345")
        self.assertTrue(logged_in)
        self.assertTrue(
            self.org_1_user_1.profiles.filter(id=self.org_1_user_1_profile.id).exists()
        )
        self.assertTrue(not hasattr(self.org_1_user_1, "active_profile"))
        response = self.client.post(
            reverse(
                "profile_activate", kwargs={"pk": str(self.org_1_user_1_profile.id)}
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.org_1_user_1_profile.organisation == self.org_1)
        self.assertTrue(
            self.org_1_user_1_profile.security_groups.filter(
                id=self.org_1_security_group_1.id
            ).exists()
        )

        required_permission = Permission.objects.get(
            organisation=self.org_1, action="EXPORT", object_type=self.object_type
        )
        self.assertIsNotNone(required_permission)
        self.assertTrue(
            self.org_1_security_group_1.permissions.filter(
                id=required_permission.id
            ).exists()
        )

        self.org_1_security_group_1.permissions.add(required_permission)

        response = self.client.get(
            reverse("model_export", kwargs={"model_id": self.org_1_model_1.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "model_export.html")
        response = self.client.post(
            reverse("model_export", kwargs={"model_id": self.org_1_model_1.id}),
            data={"export_format": "JSON"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["content-type"], "application/json")
        self.assertEqual(
            response["Content-Disposition"], "attachment; filename=export.json"
        )
        self.assertEqual(
            json.loads(response.content),
            {
                "instances": [
                    {
                        "id": str(self.instance_1.id),
                        "name": "instance_1",
                        "concept": str(self.org_1_concept_1.id),
                        "model": str(self.org_1_model_1.id),
                        "quality": "PROPOSED",
                        "status": "ACTIVE",
                        "properties": [],
                    },
                    {
                        "id": str(self.instance_2.id),
                        "name": "instance_2",
                        "concept": str(self.org_1_concept_1.id),
                        "model": str(self.org_1_model_1.id),
                        "quality": "PROPOSED",
                        "status": "ACTIVE",
                        "properties": [],
                    },
                ]
            },
        )
        response = self.client.post(
            reverse("model_export", kwargs={"model_id": self.org_1_model_1.id}),
            data={
                "export_format": "JSON",
                "selected_instances": [str(self.instance_1.id)],
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["content-type"], "application/json")
        self.assertEqual(
            response["Content-Disposition"], "attachment; filename=export.json"
        )

        self.assertEqual(
            json.loads(response.content),
            {
                "instances": [
                    {
                        "id": str(self.instance_1.id),
                        "name": "instance_1",
                        "concept": str(self.org_1_concept_1.id),
                        "model": str(self.org_1_model_1.id),
                        "quality": "PROPOSED",
                        "status": "ACTIVE",
                        "properties": [],
                    }
                ]
            },
        )
        response = self.client.post(
            reverse("model_export", kwargs={"model_id": self.org_1_model_1.id}),
            data={
                "export_format": "JSON",
                "selected_instances": [str(self.instance_1.id)],
                "_schedule_export": "Schedule Export",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/task/list/")
        self.assertEqual(response["content-type"], "text/html; charset=utf-8")
        self.assertEqual(
            response["Content-Disposition"], "attachment; filename=export.json"
        )
