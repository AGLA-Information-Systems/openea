from django.test import TestCase
from django.urls import reverse

class ProfileListTestCase(TestCase):
    def setUp(self):
        pass

    def test_profile_list_page(self):
        response = self.client.get(reverse('profile_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile/profile_list.html')