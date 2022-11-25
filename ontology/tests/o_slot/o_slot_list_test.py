from django.test import TestCase
from django.urls import reverse

class OSlotListTestCase(TestCase):
    def setUp(self):
        pass

    def test_o_slot_list_page(self):
        response = self.client.get(reverse('o_slot_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'o_slot/o_slot_list.html')