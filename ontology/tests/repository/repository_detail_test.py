from django.test import TestCase
from django.urls import reverse

class RepositoryDetailTestCase(TestCase):
    def setUp(self):
        pass

    def test_repository_detail_page(self):
        response = self.client.get(reverse('repository_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'repository/repository_detail.html')