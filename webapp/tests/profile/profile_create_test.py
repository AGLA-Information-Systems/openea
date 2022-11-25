from django.test import TestCase
from django.urls import reverse

class ProfileCreateTestCase(TestCase):
    def setUp(self):
        pass

    def test_profile_create_page(self):
        response = self.client.get(reverse('profile_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile/profile_create.html')