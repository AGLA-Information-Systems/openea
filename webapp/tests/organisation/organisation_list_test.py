from django.test import TestCase
from django.urls import reverse

class OrganisationListTestCase(TestCase):
    def setUp(self):
        pass

    def test_organisation_list_page(self):
        response = self.client.get(reverse('organisation_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'organisation/organisation_list.html')