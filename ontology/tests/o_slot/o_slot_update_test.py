from django.test import TestCase
from django.urls import reverse

class OSlotUpdateTestCase(TestCase):
    def setUp(self):
        pass

    def test_o_slot_update_page(self):
        response = self.client.get(reverse('o_slot_update'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'o_slot/o_slot_update.html')