from django.test import TestCase
from django.urls import reverse

class RepositoryListTestCase(TestCase):
    def setUp(self):
        pass

    def test_repository_list_page(self):
        response = self.client.get(reverse('repository_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'repository/repository_list.html')