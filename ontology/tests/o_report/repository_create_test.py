from django.test import TestCase
from django.urls import reverse

class RepositoryCreateTestCase(TestCase):
    def setUp(self):
        pass

    def test_repository_create_page(self):
        response = self.client.get(reverse('repository_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'repository/repository_create.html')