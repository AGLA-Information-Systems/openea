from django.test import TestCase
from django.urls import reverse

class TaskDeleteTestCase(TestCase):
    def setUp(self):
        pass

    def test_task_delete_page(self):
        response = self.client.get(reverse('task_delete'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task/task_delete.html')