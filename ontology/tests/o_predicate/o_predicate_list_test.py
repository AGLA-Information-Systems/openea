from django.test import TestCase
from django.urls import reverse

class OPredicateListTestCase(TestCase):
    def setUp(self):
        pass

    def test_o_predicate_list_page(self):
        response = self.client.get(reverse('o_predicate_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'o_predicate/o_predicate_list.html')