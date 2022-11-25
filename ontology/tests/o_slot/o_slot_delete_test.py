from django.test import TestCase
from django.urls import reverse

class OSlotDeleteTestCase(TestCase):
    def setUp(self):
        pass

    def test_o_slot_delete_page(self):
        response = self.client.get(reverse('o_slot_delete'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'o_slot/o_slot_delete.html')