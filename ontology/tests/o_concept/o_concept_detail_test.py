from django.test import TestCase
from django.urls import reverse

class OConceptDetailTestCase(TestCase):
    def setUp(self):
        pass

    def test_o_concept_detail_page(self):
        response = self.client.get(reverse('o_concept_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'o_concept/o_concept_detail.html')