from django.test import TestCase
from django.urls import reverse

class TaskDetailTestCase(TestCase):
    def setUp(self):
        pass

    def test_task_detail_page(self):
        response = self.client.get(reverse('task_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task/task_detail.html')