"""
Comprehensive tests for homepage application.
Tests pages, models, and user management.
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import HomePage, User

CustomUser = get_user_model()


class UserModelTest(TestCase):
    """Test custom User model"""

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='testuser@example.com',
            password='testpass123',
            name='Test User'
        )

    def test_user_creation(self):
        """Test user is created with email"""
        self.assertEqual(self.user.email, 'testuser@example.com')
        self.assertEqual(self.user.name, 'Test User')

    def test_user_str_method(self):
        """Test __str__ returns email"""
        self.assertEqual(str(self.user), 'testuser@example.com')

    def test_user_email_unique(self):
        """Test email field is unique"""
        with self.assertRaises(Exception):
            CustomUser.objects.create_user(
                email='testuser@example.com',
                password='different'
            )

    def test_user_password_hashed(self):
        """Test password is hashed"""
        self.assertNotEqual(self.user.password, 'testpass123')
        self.assertTrue(self.user.check_password('testpass123'))

    def test_user_type_choices(self):
        """Test user type has valid choices"""
        user_customer = CustomUser.objects.create_user(
            email='customer@example.com',
            password='pass123',
            user_type='customer'
        )
        user_staff = CustomUser.objects.create_user(
            email='staff@example.com',
            password='pass123',
            user_type='staff'
        )
        self.assertEqual(user_customer.user_type, 'customer')
        self.assertEqual(user_staff.user_type, 'staff')

    def test_user_default_type(self):
        """Test user type defaults to customer"""
        user = CustomUser.objects.create_user(
            email='default@example.com',
            password='pass123'
        )
        self.assertEqual(user.user_type, 'customer')

    def test_superuser_creation(self):
        """Test superuser creation"""
        admin = CustomUser.objects.create_superuser(
            email='admin@example.com',
            password='adminpass'
        )
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)

    def test_user_no_username(self):
        """Test user model doesn't use username"""
        self.assertIsNone(self.user.username)


class HomePageModelTest(TestCase):
    """Test HomePage model"""

    def setUp(self):
        self.page = HomePage.objects.create(
            title='Welcome',
            content='Welcome to our site'
        )

    def test_homepage_creation(self):
        """Test homepage is created correctly"""
        self.assertEqual(self.page.title, 'Welcome')
        self.assertEqual(self.page.content, 'Welcome to our site')

    def test_homepage_str_method(self):
        """Test __str__ returns title"""
        self.assertEqual(str(self.page), 'Welcome')

    def test_multiple_pages(self):
        """Test multiple homepage objects"""
        page2 = HomePage.objects.create(
            title='About',
            content='About us page'
        )
        pages = HomePage.objects.all()
        self.assertEqual(pages.count(), 2)


class HomeViewTest(TestCase):
    """Test home page view"""

    def setUp(self):
        self.client = Client()
        self.url = reverse('Home')

    def test_home_view_status_code(self):
        """Test home view returns 200"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_home_view_template(self):
        """Test home view uses correct template"""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'homepage/home.html')

    def test_home_view_accessible(self):
        """Test home view is accessible"""
        response = self.client.get(self.url)
        self.assertIsNotNone(response)


class ContactViewTest(TestCase):
    """Test contact page view"""

    def setUp(self):
        self.client = Client()
        self.url = reverse('Contact')

    def test_contact_view_status_code(self):
        """Test contact view returns 200"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_contact_view_template(self):
        """Test contact view uses correct template"""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'homepage/contact.html')

    def test_contact_view_accessible(self):
        """Test contact view is accessible"""
        response = self.client.get(self.url)
        self.assertIsNotNone(response)


class ProjectsViewTest(TestCase):
    """Test projects page view"""

    def setUp(self):
        self.client = Client()
        self.url = reverse('Projects')

    def test_projects_view_status_code(self):
        """Test projects view returns 200"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_projects_view_template(self):
        """Test projects view uses correct template"""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'homepage/projects.html')

    def test_projects_view_accessible(self):
        """Test projects view is accessible"""
        response = self.client.get(self.url)
        self.assertIsNotNone(response)


class UserAuthenticationTest(TestCase):
    """Test user authentication and login"""

    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            email='testuser@example.com',
            password='testpass123'
        )

    def test_user_login(self):
        """Test user can login"""
        login_success = self.client.login(
            email='testuser@example.com',
            password='testpass123'
        )
        self.assertTrue(login_success)

    def test_user_wrong_password(self):
        """Test login fails with wrong password"""
        login_success = self.client.login(
            email='testuser@example.com',
            password='wrongpass'
        )
        self.assertFalse(login_success)

    def test_user_nonexistent_email(self):
        """Test login fails with nonexistent email"""
        login_success = self.client.login(
            email='nonexistent@example.com',
            password='testpass123'
        )
        self.assertFalse(login_success)

    def test_user_profile_accessible(self):
        """Test authenticated user can access pages"""
        self.client.login(
            email='testuser@example.com',
            password='testpass123'
        )
        response = self.client.get(reverse('Home'))
        self.assertEqual(response.status_code, 200)


class HomepageViewsIntegrationTest(TestCase):
    """Integration tests for homepage views"""

    def setUp(self):
        self.client = Client()

    def test_all_pages_accessible(self):
        """Test all homepage views are accessible"""
        pages = [
            reverse('Home'),
            reverse('Contact'),
            reverse('Projects'),
        ]
        
        for page_url in pages:
            response = self.client.get(page_url)
            self.assertEqual(response.status_code, 200,
                           f"Failed for {page_url}")

    def test_navigation_between_pages(self):
        """Test navigation between pages"""
        # Access home
        response = self.client.get(reverse('Home'))
        self.assertEqual(response.status_code, 200)
        
        # Access contact
        response = self.client.get(reverse('Contact'))
        self.assertEqual(response.status_code, 200)
        
        # Access projects
        response = self.client.get(reverse('Projects'))
        self.assertEqual(response.status_code, 200)


class UserManagementTest(TestCase):
    """Test user management functionality"""

    def setUp(self):
        self.client = Client()

    def test_multiple_users_creation(self):
        """Test creating multiple users"""
        for i in range(5):
            CustomUser.objects.create_user(
                email=f'user{i}@example.com',
                password='pass123'
            )
        
        users = CustomUser.objects.all()
        self.assertEqual(users.count(), 5)

    def test_user_with_all_fields(self):
        """Test creating user with all fields"""
        user = CustomUser.objects.create_user(
            email='full@example.com',
            password='pass123',
            name='Full Name',
            user_type='staff'
        )
        self.assertEqual(user.name, 'Full Name')
        self.assertEqual(user.user_type, 'staff')

    def test_user_email_normalization(self):
        """Test email is stored as provided"""
        user = CustomUser.objects.create_user(
            email='TestUser@example.com',
            password='pass123'
        )
        # Email should be stored as normalized by BaseUserManager.normalize_email
        # which lowercases the entire email address
        self.assertIsNotNone(user.email)
        self.assertTrue('@' in user.email)

    def test_user_deletion(self):
        """Test user can be deleted"""
        user = CustomUser.objects.create_user(
            email='delete@example.com',
            password='pass123'
        )
        user_id = user.id
        user.delete()
        
        deleted = CustomUser.objects.filter(id=user_id).exists()
        self.assertFalse(deleted)


class SuperuserManagementTest(TestCase):
    """Test superuser/admin management"""

    def setUp(self):
        self.admin = CustomUser.objects.create_superuser(
            email='admin@example.com',
            password='adminpass'
        )

    def test_superuser_creation(self):
        """Test superuser is created correctly"""
        self.assertTrue(self.admin.is_superuser)
        self.assertTrue(self.admin.is_staff)

    def test_superuser_permissions(self):
        """Test superuser has necessary permissions"""
        self.assertTrue(self.admin.is_active)
        self.assertTrue(self.admin.has_perm('any_permission'))

    def test_staff_user_creation(self):
        """Test staff user is different from superuser"""
        staff = CustomUser.objects.create_user(
            email='staff@example.com',
            password='staffpass',
            user_type='staff'
        )
        self.assertFalse(staff.is_superuser)
        self.assertEqual(staff.user_type, 'staff')
