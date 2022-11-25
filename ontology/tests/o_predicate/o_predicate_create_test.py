from django.test import TestCase
from django.urls import reverse

class OPredicateCreateTestCase(TestCase):
    def setUp(self):
        pass

    def test_o_predicate_create_page(self):
        response = self.client.get(reverse('o_predicate_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'o_predicate/o_predicate_create.html')