from django.test import TestCase
from django.urls import reverse

class ProfileDetailTestCase(TestCase):
    def setUp(self):
        pass

    def test_profile_detail_page(self):
        response = self.client.get(reverse('profile_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile/profile_detail.html')