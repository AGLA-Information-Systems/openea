from django.test import TestCase
from django.urls import reverse

class TaskCreateTestCase(TestCase):
    def setUp(self):
        pass

    def test_task_create_page(self):
        response = self.client.get(reverse('task_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task/task_create.html')