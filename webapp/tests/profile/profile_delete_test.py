from django.test import TestCase
from django.urls import reverse

class ProfileDeleteTestCase(TestCase):
    def setUp(self):
        pass

    def test_profile_delete_page(self):
        response = self.client.get(reverse('profile_delete'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile/profile_delete.html')