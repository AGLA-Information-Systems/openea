from django.test import TestCase
from django.urls import reverse

class TaskUpdateTestCase(TestCase):
    def setUp(self):
        pass

    def test_task_update_page(self):
        response = self.client.get(reverse('task_update'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task/task_update.html')