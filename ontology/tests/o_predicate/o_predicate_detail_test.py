from django.test import TestCase
from django.urls import reverse

class OPredicateDetailTestCase(TestCase):
    def setUp(self):
        pass

    def test_o_predicate_detail_page(self):
        response = self.client.get(reverse('o_predicate_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'o_predicate/o_predicate_detail.html')