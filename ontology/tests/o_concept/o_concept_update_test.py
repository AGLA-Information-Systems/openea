from django.test import TestCase
from django.urls import reverse

class OConceptUpdateTestCase(TestCase):
    def setUp(self):
        pass

    def test_o_concept_update_page(self):
        response = self.client.get(reverse('o_concept_update'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'o_concept/o_concept_update.html')