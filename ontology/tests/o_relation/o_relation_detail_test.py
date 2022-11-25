from django.test import TestCase
from django.urls import reverse

class ORelationDetailTestCase(TestCase):
    def setUp(self):
        pass

    def test_o_relation_detail_page(self):
        response = self.client.get(reverse('o_relation_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'o_relation/o_relation_detail.html')