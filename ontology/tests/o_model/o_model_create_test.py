from django.test import TestCase
from django.urls import reverse

class OModelCreateTestCase(TestCase):
    def setUp(self):
        pass

    def test_o_model_create_page(self):
        response = self.client.get(reverse('o_model_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'o_model/o_model_create.html')