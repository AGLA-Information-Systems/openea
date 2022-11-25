from django.test import TestCase
from django.urls import reverse

class OPredicateUpdateTestCase(TestCase):
    def setUp(self):
        pass

    def test_o_predicate_update_page(self):
        response = self.client.get(reverse('o_predicate_update'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'o_predicate/o_predicate_update.html')