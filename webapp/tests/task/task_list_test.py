from django.test import TestCase
from django.urls import reverse

class TaskListTestCase(TestCase):
    def setUp(self):
        pass

    def test_task_list_page(self):
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task/task_list.html')