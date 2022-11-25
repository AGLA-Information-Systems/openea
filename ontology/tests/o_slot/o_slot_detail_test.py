from django.test import TestCase
from django.urls import reverse

class OSlotDetailTestCase(TestCase):
    def setUp(self):
        pass

    def test_o_slot_detail_page(self):
        response = self.client.get(reverse('o_slot_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'o_slot/o_slot_detail.html')