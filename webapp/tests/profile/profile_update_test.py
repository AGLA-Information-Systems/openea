from django.test import TestCase
from django.urls import reverse

class ProfileUpdateTestCase(TestCase):
    def setUp(self):
        pass

    def test_profile_update_page(self):
        response = self.client.get(reverse('profile_update'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile/profile_update.html')