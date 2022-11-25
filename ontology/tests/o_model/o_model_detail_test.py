from django.test import TestCase
from django.urls import reverse

class OModelDetailTestCase(TestCase):
    def setUp(self):
        pass

    def test_o_model_detail_page(self):
        response = self.client.get(reverse('o_model_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'o_model/o_model_detail.html')