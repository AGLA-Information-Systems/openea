from django.test import TestCase
from django.urls import reverse

class RepositoryDeleteTestCase(TestCase):
    def setUp(self):
        pass

    def test_repository_delete_page(self):
        response = self.client.get(reverse('repository_delete'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'repository/repository_delete.html')