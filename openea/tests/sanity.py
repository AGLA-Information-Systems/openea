from django.test import TestCase
from django.urls import reverse

class SanityTestCase(TestCase):
    def setUp(self):
        pass

    def test_o_concept_create_page(self):
        response = self.client.get(reverse('o_concept_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'o_concept/o_concept_create.html')