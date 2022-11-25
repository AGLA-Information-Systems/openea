from django.test import TestCase
from django.urls import reverse

class OrganisationDetailTestCase(TestCase):
    def setUp(self):
        pass

    def test_organisation_detail_page(self):
        response = self.client.get(reverse('organisation_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'organisation/organisation_detail.html')