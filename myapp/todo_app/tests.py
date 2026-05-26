
"""
Comprehensive tests for todo_app application.
Tests models, views, and forms functionality.
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from datetime import date, timedelta
from .models import Category, TodoItemStatus, Priority, TodoItem, UserTodo
from .forms import TodoItemForm

User = get_user_model()


class CategoryModelTest(TestCase):
    """Test Category model"""

    def setUp(self):
        self.category = Category.objects.create(name='Work')

    def test_category_creation(self):
        """Test category is created with correct name"""
        self.assertEqual(self.category.name, 'Work')
        self.assertEqual(str(self.category), 'Work')

    def test_category_str_method(self):
        """Test __str__ method returns category name"""
        self.assertEqual(str(self.category), 'Work')

    def test_category_verbose_name_plural(self):
        """Test verbose name plural is correct"""
        self.assertEqual(Category._meta.verbose_name_plural, 'Categories')


class TodoItemStatusModelTest(TestCase):
    """Test TodoItemStatus model"""

    def setUp(self):
        self.status = TodoItemStatus.objects.create(name='Pending')

    def test_status_creation(self):
        """Test status is created with correct name"""
        self.assertEqual(self.status.name, 'Pending')
        self.assertEqual(str(self.status), 'Pending')

    def test_status_str_method(self):
        """Test __str__ method returns status name"""
        self.assertEqual(str(self.status), 'Pending')


class PriorityModelTest(TestCase):
    """Test Priority model"""

    def setUp(self):
        self.priority = Priority.objects.create(level=1)

    def test_priority_creation(self):
        """Test priority is created with correct level"""
        self.assertEqual(self.priority.level, 1)
        self.assertEqual(str(self.priority), 'Priority 1')

    def test_priority_uniqueness(self):
        """Test priority levels are unique"""
        with self.assertRaises(Exception):
            Priority.objects.create(level=1)


class TodoItemModelTest(TestCase):
    """Test TodoItem model"""

    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(name='Personal')
        self.status = TodoItemStatus.objects.create(name='In Progress')
        self.priority = Priority.objects.create(level=1)
        
        self.todo = TodoItem.objects.create(
            name='Test Task',
            description='This is a test task',
            category=self.category,
            user=self.user,
            status=self.status,
            priority=self.priority,
            due_date=date.today() + timedelta(days=7)
        )

    def test_todo_item_creation(self):
        """Test todo item is created correctly"""
        self.assertEqual(self.todo.name, 'Test Task')
        self.assertEqual(self.todo.description, 'This is a test task')
        self.assertEqual(self.todo.user, self.user)
        self.assertEqual(self.todo.category, self.category)

    def test_todo_item_str_method(self):
        """Test __str__ method returns todo name"""
        self.assertEqual(str(self.todo), 'Test Task')

    def test_todo_item_ordering(self):
        """Test todo items are ordered by created_at descending"""
        todo2 = TodoItem.objects.create(name='Task 2')
        todos = TodoItem.objects.all()
        self.assertEqual(todos[0], todo2)

    def test_todo_item_default_values(self):
        """Test todo item default values"""
        todo_minimal = TodoItem.objects.create(name='Minimal Task')
        self.assertIsNone(todo_minimal.user)
        self.assertIsNone(todo_minimal.category)
        self.assertIsNotNone(todo_minimal.created_at)

    def test_todo_item_dudate_optional(self):
        """Test due_date is optional"""
        todo_no_date = TodoItem.objects.create(name='No Date Task')
        self.assertIsNone(todo_no_date.due_date)


class UserTodoModelTest(TestCase):
    """Test UserTodo model"""

    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpass123'
        )
        self.todo = TodoItem.objects.create(name='Test Task')
        self.user_todo = UserTodo.objects.create(
            user=self.user,
            todo_item=self.todo
        )

    def test_user_todo_creation(self):
        """Test user todo relationship is created"""
        self.assertEqual(self.user_todo.user, self.user)
        self.assertEqual(self.user_todo.todo_item, self.todo)

    def test_user_todo_str_method(self):
        """Test __str__ method formats correctly"""
        expected = f"{self.user} - {self.todo}"
        self.assertEqual(str(self.user_todo), expected)

    def test_user_todo_cascade_delete(self):
        """Test cascading delete when user is deleted"""
        user_todo_id = self.user_todo.id
        self.user.delete()
        self.assertFalse(UserTodo.objects.filter(id=user_todo_id).exists())


class TodoItemFormTest(TestCase):
    """Test TodoItemForm"""

    def setUp(self):
        self.category = Category.objects.create(name='Work')
        self.status = TodoItemStatus.objects.create(name='Pending')
        self.priority = Priority.objects.create(level=1)

    def test_form_valid_data(self):
        """Test form with valid data"""
        form_data = {
            'name': 'New Task',
            'description': 'Task description',
            'category': self.category.id,
            'status': self.status.id,
            'priority': self.priority.id,
            'due_date': date.today() + timedelta(days=7)
        }
        form = TodoItemForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_no_name(self):
        """Test form validation requires name"""
        form_data = {
            'description': 'Task without name',
        }
        form = TodoItemForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_minimal_data(self):
        """Test form with minimal required data"""
        form_data = {
            'name': 'Minimal Task',
        }
        form = TodoItemForm(data=form_data)
        self.assertTrue(form.is_valid())


class TodoListViewTest(TestCase):
    """Test TodoListView"""

    def setUp(self):
        self.client = Client()
        self.url = reverse('todo_list')
        
        # Create test todos
        for i in range(15):
            TodoItem.objects.create(name=f'Task {i+1}')

    def test_todo_list_view_status_code(self):
        """Test todo list view returns 200"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_todo_list_view_template(self):
        """Test todo list view uses correct template"""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'todo_app/todo_list.html')

    def test_todo_list_view_context(self):
        """Test todo list view has correct context"""
        response = self.client.get(self.url)
        self.assertIn('todos', response.context)

    def test_todo_list_pagination(self):
        """Test todo list view paginates correctly"""
        response = self.client.get(self.url)
        self.assertEqual(len(response.context['todos']), 10)

    def test_todo_list_pagination_second_page(self):
        """Test second page of pagination"""
        response = self.client.get(self.url + '?page=2')
        self.assertEqual(len(response.context['todos']), 5)


class TodoDetailViewTest(TestCase):
    """Test TodoDetailView"""

    def setUp(self):
        self.client = Client()
        self.todo = TodoItem.objects.create(name='Detail Test Task')
        self.url = reverse('todo_detail', kwargs={'pk': self.todo.pk})

    def test_todo_detail_view_exists(self):
        """Test todo detail view returns 200"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_todo_detail_view_template(self):
        """Test todo detail view uses correct template"""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'todo_app/todo_detail.html')

    def test_todo_detail_view_context(self):
        """Test todo detail view has todo in context"""
        response = self.client.get(self.url)
        self.assertEqual(response.context['todo'], self.todo)

    def test_todo_detail_view_invalid_id(self):
        """Test todo detail view with invalid todo id"""
        invalid_url = reverse('todo_detail', kwargs={'pk': 99999})
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, 404)


class TodoCreateViewTest(TestCase):
    """Test TodoCreateView"""

    def setUp(self):
        self.client = Client()
        self.url = reverse('todo_create')
        self.category = Category.objects.create(name='Work')

    def test_create_view_get_status_code(self):
        """Test create view GET returns 200"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        """Test create view uses correct template"""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'todo_app/todo_form.html')

    def test_create_todo_post(self):
        """Test creating todo via POST"""
        data = {
            'name': 'New Todo',
            'description': 'Test todo description',
            'category': self.category.id,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(TodoItem.objects.filter(name='New Todo').exists())

    def test_create_todo_redirect(self):
        """Test create view redirects to todo list"""
        data = {'name': 'New Todo'}
        response = self.client.post(self.url, data)
        self.assertRedirects(response, reverse('todo_list'))


class TodoUpdateViewTest(TestCase):
    """Test TodoUpdateView"""

    def setUp(self):
        self.client = Client()
        self.todo = TodoItem.objects.create(
            name='Original Name',
            description='Original description'
        )
        self.url = reverse('todo_update', kwargs={'pk': self.todo.pk})

    def test_update_view_get_status_code(self):
        """Test update view GET returns 200"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_todo_post(self):
        """Test updating todo via POST"""
        data = {
            'name': 'Updated Name',
            'description': 'Updated description'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.todo.refresh_from_db()
        self.assertEqual(self.todo.name, 'Updated Name')

    def test_update_todo_redirect(self):
        """Test update view redirects to todo list"""
        data = {'name': 'Updated Name'}
        response = self.client.post(self.url, data)
        self.assertRedirects(response, reverse('todo_list'))


class TodoDeleteViewTest(TestCase):
    """Test TodoDeleteView"""

    def setUp(self):
        self.client = Client()
        self.todo = TodoItem.objects.create(name='Delete Me')
        self.url = reverse('todo_delete', kwargs={'pk': self.todo.pk})

    def test_delete_view_get_status_code(self):
        """Test delete view GET returns 200"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_delete_todo_post(self):
        """Test deleting todo via POST"""
        todo_id = self.todo.id
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(TodoItem.objects.filter(id=todo_id).exists())

    def test_delete_todo_redirect(self):
        """Test delete view redirects to todo list"""
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('todo_list'))


class TodoIntegrationTest(TestCase):
    """Integration tests for todo app workflow"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpass123'
        )

    def test_complete_todo_workflow(self):
        """Test creating, viewing, updating, and deleting a todo"""
        # Create
        create_url = reverse('todo_create')
        create_data = {'name': 'Workflow Test Task'}
        response = self.client.post(create_url, create_data)
        self.assertEqual(response.status_code, 302)
        
        # Retrieve
        todo = TodoItem.objects.get(name='Workflow Test Task')
        detail_url = reverse('todo_detail', kwargs={'pk': todo.pk})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, 200)
        
        # Update
        update_url = reverse('todo_update', kwargs={'pk': todo.pk})
        update_data = {'name': 'Updated Workflow Task'}
        response = self.client.post(update_url, update_data)
        self.assertEqual(response.status_code, 302)
        
        # Delete
        delete_url = reverse('todo_delete', kwargs={'pk': todo.pk})
        response = self.client.post(delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(TodoItem.objects.filter(pk=todo.pk).exists())
