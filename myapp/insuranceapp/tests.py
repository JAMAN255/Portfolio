"""
Comprehensive tests for insuranceapp application.
Tests insurance models, views, and forms.
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from decimal import Decimal
from .models import (
    InsCategory, Price, InsuranceStatus, Insurance, 
    CustomerProfile, StaffProfile
)

User = get_user_model()


class InsCategoryModelTest(TestCase):
    """Test InsCategory model"""

    def setUp(self):
        self.category = InsCategory.objects.create(name='Health')

    def test_category_creation(self):
        """Test category is created with correct name"""
        self.assertEqual(self.category.name, 'Health')

    def test_category_str_method(self):
        """Test __str__ returns category name"""
        self.assertEqual(str(self.category), 'Health')

    def test_multiple_categories(self):
        """Test creating multiple categories"""
        InsCategory.objects.create(name='Auto')
        InsCategory.objects.create(name='Home')
        
        categories = InsCategory.objects.all()
        self.assertEqual(categories.count(), 3)


class PriceModelTest(TestCase):
    """Test Price model"""

    def setUp(self):
        self.price = Price.objects.create(
            amount=Decimal('99.99'),
            currency='USD'
        )

    def test_price_creation(self):
        """Test price is created correctly"""
        self.assertEqual(self.price.amount, Decimal('99.99'))
        self.assertEqual(self.price.currency, 'USD')

    def test_price_str_method(self):
        """Test __str__ returns formatted price"""
        expected = f"{self.price.amount} {self.price.currency}"
        self.assertEqual(str(self.price), expected)

    def test_price_decimal_precision(self):
        """Test decimal precision is maintained"""
        price = Price.objects.create(
            amount=Decimal('1000.50'),
            currency='EUR'
        )
        self.assertEqual(price.amount, Decimal('1000.50'))

    def test_multiple_currencies(self):
        """Test prices with different currencies"""
        USD = Price.objects.create(amount=Decimal('100'), currency='USD')
        EUR = Price.objects.create(amount=Decimal('100'), currency='EUR')
        GBP = Price.objects.create(amount=Decimal('100'), currency='GBP')
        
        self.assertEqual(USD.currency, 'USD')
        self.assertEqual(EUR.currency, 'EUR')
        self.assertEqual(GBP.currency, 'GBP')


class InsuranceStatusModelTest(TestCase):
    """Test InsuranceStatus model"""

    def setUp(self):
        self.active_status = InsuranceStatus.objects.create(status='active')
        self.inactive_status = InsuranceStatus.objects.create(status='inactive')

    def test_status_creation(self):
        """Test status is created correctly"""
        self.assertEqual(self.active_status.status, 'active')
        self.assertEqual(self.inactive_status.status, 'inactive')

    def test_status_str_method(self):
        """Test __str__ returns status"""
        self.assertEqual(str(self.active_status), 'active')
        self.assertEqual(str(self.inactive_status), 'inactive')

    def test_default_status(self):
        """Test default status is inactive"""
        status = InsuranceStatus()
        self.assertEqual(status.status, 'inactive')

    def test_invalid_status_choice(self):
        """Test invalid status choice is rejected"""
        with self.assertRaises(Exception):
            status = InsuranceStatus.objects.create(status='pending')


class InsuranceModelTest(TestCase):
    """Test Insurance model"""

    def setUp(self):
        self.category = InsCategory.objects.create(name='Health')
        self.price = Price.objects.create(
            amount=Decimal('500.00'),
            currency='USD'
        )
        self.status = InsuranceStatus.objects.create(status='active')
        
        self.insurance = Insurance.objects.create(
            name='Premium Health Insurance',
            description='Comprehensive health coverage',
            ins_category=self.category,
            price=self.price,
            status=self.status
        )

    def test_insurance_creation(self):
        """Test insurance is created correctly"""
        self.assertEqual(self.insurance.name, 'Premium Health Insurance')
        self.assertEqual(self.insurance.description, 'Comprehensive health coverage')
        self.assertEqual(self.insurance.ins_category, self.category)
        self.assertEqual(self.insurance.price, self.price)

    def test_insurance_str_method(self):
        """Test __str__ returns insurance name"""
        self.assertEqual(str(self.insurance), 'Premium Health Insurance')

    def test_insurance_optional_fields(self):
        """Test optional fields in insurance"""
        insurance = Insurance.objects.create(name='Basic Plan')
        self.assertIsNone(insurance.description)
        self.assertIsNone(insurance.ins_category)
        self.assertIsNone(insurance.price)

    def test_insurance_create_method(self):
        """Test create_insurance method"""
        new_insurance = self.insurance.create_insurance(
            name='New Plan',
            descrption='New insurance plan',
            price=self.price,
            category=self.category
        )
        self.assertEqual(new_insurance.name, 'New Plan')
        self.assertIsNotNone(new_insurance.id)

    def test_multiple_insurances(self):
        """Test multiple insurance objects"""
        insurance2 = Insurance.objects.create(
            name='Auto Insurance',
            ins_category=self.category
        )
        insurances = Insurance.objects.all()
        self.assertEqual(insurances.count(), 2)

    def test_insurance_cascade_delete_category(self):
        """Test insurance is deleted when category is deleted"""
        insurance_id = self.insurance.id
        self.category.delete()
        self.assertFalse(Insurance.objects.filter(id=insurance_id).exists())


class CustomerProfileModelTest(TestCase):
    """Test CustomerProfile model"""

    def setUp(self):
        self.user = User.objects.create_user(
            email='customer@example.com',
            password='testpass123'
        )
        self.profile = CustomerProfile.objects.create(
            user=self.user,
            policy_number='POL123456',
            email='customer@example.com',
            first_name='John',
            last_name='Doe'
        )

    def test_customer_profile_creation(self):
        """Test customer profile is created"""
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.profile.policy_number, 'POL123456')
        self.assertEqual(self.profile.first_name, 'John')
        self.assertEqual(self.profile.last_name, 'Doe')

    def test_customer_profile_one_to_one(self):
        """Test one-to-one relationship with user"""
        profile = self.user.customer_profile
        self.assertEqual(profile, self.profile)

    def test_customer_profile_cascade_delete_user(self):
        """Test profile is deleted when user is deleted"""
        profile_id = self.profile.id
        self.user.delete()
        self.assertFalse(CustomerProfile.objects.filter(id=profile_id).exists())


class StaffProfileModelTest(TestCase):
    """Test StaffProfile model"""

    def setUp(self):
        self.user = User.objects.create_user(
            email='staff@example.com',
            password='testpass123',
            user_type='staff'
        )
        self.profile = StaffProfile.objects.create(
            user=self.user,
            department='Sales'
        )

    def test_staff_profile_creation(self):
        """Test staff profile is created"""
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.profile.department, 'Sales')

    def test_staff_profile_one_to_one(self):
        """Test one-to-one relationship with user"""
        profile = self.user.staff_profile
        self.assertEqual(profile, self.profile)

    def test_multiple_staff_profiles(self):
        """Test multiple staff profiles"""
        user2 = User.objects.create_user(
            email='staff2@example.com',
            password='pass123'
        )
        StaffProfile.objects.create(
            user=user2,
            department='Support'
        )
        profiles = StaffProfile.objects.all()
        self.assertEqual(profiles.count(), 2)


class InsuranceListViewTest(TestCase):
    """Test InsuranceListView"""

    def setUp(self):
        self.client = Client()
        self.url = reverse('insurance_list')
        
        category = InsCategory.objects.create(name='Health')
        for i in range(5):
            Insurance.objects.create(
                name=f'Insurance {i+1}',
                ins_category=category
            )

    def test_insurance_list_status_code(self):
        """Test insurance list view returns 200"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_insurance_list_template(self):
        """Test insurance list uses correct template"""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'insurance_app/insurance_list.html')

    def test_insurance_list_context(self):
        """Test insurance list has insurances in context"""
        response = self.client.get(self.url)
        self.assertIn('insurance', response.context)

    def test_insurance_list_display_all(self):
        """Test all insurances are displayed"""
        response = self.client.get(self.url)
        self.assertEqual(len(response.context['insurance']), 5)


class InsuranceDetailViewTest(TestCase):
    """Test InsuranceDetailView"""

    def setUp(self):
        self.client = Client()
        self.insurance = Insurance.objects.create(name='Test Insurance')
        self.url = reverse('insurance_detail', kwargs={'pk': self.insurance.pk})

    def test_insurance_detail_status_code(self):
        """Test insurance detail view returns 200"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_insurance_detail_template(self):
        """Test insurance detail uses correct template"""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'insurance_app/insurance_detail.html')

    def test_insurance_detail_context(self):
        """Test insurance detail has insurance in context"""
        response = self.client.get(self.url)
        self.assertEqual(response.context['insurance'], self.insurance)


class InsuranceCreateViewTest(TestCase):
    """Test InsuranceCreateView"""

    def setUp(self):
        self.client = Client()
        self.url = reverse('insurance_create')
        self.category = InsCategory.objects.create(name='Auto')

    def test_create_view_status_code(self):
        """Test create view GET returns 200"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        """Test create view uses correct template"""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'insurance_app/insurance_form.html')

    def test_create_insurance_post(self):
        """Test creating insurance via POST"""
        data = {
            'name': 'New Auto Insurance',
            'description': 'Complete auto coverage',
            'ins_category': self.category.id
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Insurance.objects.filter(name='New Auto Insurance').exists())

    def test_create_insurance_redirect(self):
        """Test create view redirects to insurance list"""
        data = {'name': 'Test Plan'}
        response = self.client.post(self.url, data)
        self.assertRedirects(response, reverse('insurance_list'))


class InsuranceUpdateViewTest(TestCase):
    """Test InsuranceUpdateView"""

    def setUp(self):
        self.client = Client()
        self.insurance = Insurance.objects.create(
            name='Original Name',
            description='Original description'
        )
        self.url = reverse('insurance_update', kwargs={'pk': self.insurance.pk})

    def test_update_view_status_code(self):
        """Test update view GET returns 200"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_insurance_post(self):
        """Test updating insurance via POST"""
        data = {
            'name': 'Updated Name',
            'description': 'Updated description'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.insurance.refresh_from_db()
        self.assertEqual(self.insurance.name, 'Updated Name')

    def test_update_insurance_redirect(self):
        """Test update view redirects to insurance list"""
        data = {'name': 'Updated Name'}
        response = self.client.post(self.url, data)
        self.assertRedirects(response, reverse('insurance_list'))


class InsuranceDeleteViewTest(TestCase):
    """Test InsuranceDeleteView"""

    def setUp(self):
        self.client = Client()
        self.insurance = Insurance.objects.create(name='Delete Me')
        self.url = reverse('insurance_delete', kwargs={'pk': self.insurance.pk})

    def test_delete_view_status_code(self):
        """Test delete view GET returns 200"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_delete_insurance_post(self):
        """Test deleting insurance via POST"""
        insurance_id = self.insurance.id
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Insurance.objects.filter(id=insurance_id).exists())

    def test_delete_redirect(self):
        """Test delete view redirects to insurance list"""
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('insurance_list'))


class InsuranceWorkflowTest(TestCase):
    """Integration tests for insurance app workflow"""

    def setUp(self):
        self.client = Client()
        self.category = InsCategory.objects.create(name='Health')

    def test_complete_insurance_workflow(self):
        """Test creating, viewing, updating, and deleting insurance"""
        # Create
        create_url = reverse('insurance_create')
        create_data = {
            'name': 'Workflow Insurance',
            'description': 'Workflow test',
            'ins_category': self.category.id
        }
        response = self.client.post(create_url, create_data)
        self.assertEqual(response.status_code, 302)
        
        # Retrieve
        insurance = Insurance.objects.get(name='Workflow Insurance')
        detail_url = reverse('insurance_detail', kwargs={'pk': insurance.pk})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, 200)
        
        # Update
        update_url = reverse('insurance_update', kwargs={'pk': insurance.pk})
        update_data = {'name': 'Updated Workflow Insurance'}
        response = self.client.post(update_url, update_data)
        self.assertEqual(response.status_code, 302)
        
        # Delete
        delete_url = reverse('insurance_delete', kwargs={'pk': insurance.pk})
        response = self.client.post(delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Insurance.objects.filter(pk=insurance.pk).exists())
