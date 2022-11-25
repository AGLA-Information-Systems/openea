from django.test import TestCase
from django.urls import reverse

class ORelationCreateTestCase(TestCase):
    def setUp(self):
        pass

    def test_o_relation_create_page(self):
        response = self.client.get(reverse('o_relation_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'o_relation/o_relation_create.html')