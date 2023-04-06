from django.test import TestCase
from django.urls import reverse

class ReportUpdateTestCase(TestCase):
    def setUp(self):
        pass

    def test_repository_update_page(self):
        response = self.client.get(reverse('repository_update'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'repository/repository_update.html')