from django.test import TestCase
from django.urls import reverse

class OrganisationUpdateTestCase(TestCase):
    def setUp(self):
        pass

    def test_organisation_update_page(self):
        response = self.client.get(reverse('organisation_update'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'organisation/organisation_update.html')