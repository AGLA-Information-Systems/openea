from django.test import TestCase
from django.urls import reverse

class OConceptListTestCase(TestCase):
    def setUp(self):
        pass

    def test_o_concept_list_page(self):
        response = self.client.get(reverse('o_concept_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'o_concept/o_concept_list.html')