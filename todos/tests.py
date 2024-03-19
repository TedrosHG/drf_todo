from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from todos.models import Todo


class TodosAPITestCase(APITestCase):

    def create_todo(self):
        sample_todo = {'title': 'test title', 'desc': 'this is a test description'}
        response = self.client.post(reverse('todos'), sample_todo)
        return  response

    def authenticate(self):
        self.client.post(reverse('register'), {
            'username': 'username', 'email': 'email@gmail.com', 'password': 'password'
        })
        response = self.client.post(reverse('login'), {
            'email': 'email@gmail.com', 'password': 'password'
        })
        self.client.credentials (HTTP_AUTHORIZATION=f'Bearer {response.data["token"]}')

class TestListCreateTodos(TodosAPITestCase):

    def test_should_not_create_todo_with_no_auth(self):
        response = self.create_todo()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_todo(self):
        self.authenticate()
        previous_todo_count = Todo.objects.all().count()
        response = self.create_todo()
        self.assertEqual(Todo.objects.all().count(), previous_todo_count+1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'test title')
        self.assertEqual(response.data['desc'], 'this is a test description')

    def test_retrieves_all_todos(self):
        self.authenticate()
        response = self.client.get(reverse('todos'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data['results'], list)

        sample_todo = {'title': 'test title', 'desc': 'this is a test description'}
        self.client.post(reverse('todos'), sample_todo)

        res = self.client.get(reverse('todos'))
        self.assertIsInstance(res.data['count'], int)
        self.assertEqual(res.data['count'], 1)

class TestTodoDetailAPIView(TodosAPITestCase):

    def test_retrieve_one_item(self):
        self.authenticate()
        response = self.create_todo()
        res = self.client.get(reverse('todo', kwargs= {
            'id': response.data['id']
        }))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        todo = Todo.objects.get(id=response.data['id'])
        self.assertEqual(todo.title, response.data['title'])

    def test_update_one_item(self):
        self.authenticate()
        response = self.create_todo()
        res = self.client.patch(reverse('todo', kwargs= {
            'id': response.data['id']
        }), {
            'title': 'new title', 'is_completed': True
        })
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        updated_todo = Todo.objects.get(id=res.data['id'])
        self.assertEqual(updated_todo.is_completed, True)
        self.assertEqual(updated_todo.title, 'new title')

    def test_delete_one_item(self):
        self.authenticate()
        response = self.create_todo()
        previous_todo_count = Todo.objects.all().count()
        self.assertEqual(previous_todo_count, 1)
        res = self.client.delete(reverse('todo', kwargs= {
            'id': response.data['id']
        }))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Todo.objects.all().count(), 0)

