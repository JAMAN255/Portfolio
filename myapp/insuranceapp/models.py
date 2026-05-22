from django.db import models
from django.conf import settings
from django.utils import timezone
# Create your models here.

class InsCategory(models.Model):
    name = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return self.name
    
class Price(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.amount} {self.currency}"
    
class InsuranceStatus(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='inactive')

    def __str__(self):
        return self.status

class Insurance(models.Model):
    name=models.CharField(max_length=100, blank=False)
    description=models.TextField(blank=True, null=True)
    ins_category = models.ForeignKey(InsCategory, on_delete=models.CASCADE, related_name='insurances', null=True, blank=True)
    price=models.ForeignKey(Price, on_delete=models.CASCADE, related_name='insurances', null=True, blank=True)
    status = models.ForeignKey(InsuranceStatus, on_delete=models.CASCADE, related_name='insurances', null=True, blank=True)

    class Meta:
        verbose_name = "insurance"
        verbose_name_plural = "insurances"

    def __str__(self):
        return self.name

    def create_insurance(self, name, description, price, ins_category=None, status=None):
        insurance = Insurance(name=name, description=description, price=price, ins_category=ins_category, status=status)
        insurance.save()
        return insurance


class CustomerProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='customer_profile'
    )
     # insurance-specific fields
    policy_number = models.CharField(max_length=50, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    first_name = models.TextField(null=True, blank=True, max_length= 100)
    last_name = models.TextField(null=True, blank=True, max_length= 100)
    email = models.EmailField(null=False, blank = False)
    name = models.TextField(max_length = 100, blank = True, null = True)
    user_type = models.TextField(max_length = 20, null=True, blank=True)
    
class StaffProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='staff_profile'
    )
    department = models.CharField(max_length=100, blank=True)


class CustomerInsurance(models.Model):
    """Model to track insurance applications and assignments for customers"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('active', 'Active'),
    ]
    
    customer = models.ForeignKey(
        'CustomerProfile',
        on_delete=models.CASCADE,
        related_name='insurance_applications'
    )
    insurance = models.ForeignKey(
        'Insurance',
        on_delete=models.CASCADE,
        related_name='customer_applications'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        unique_together = ('customer', 'insurance')
        verbose_name_plural = "Customer Insurances"
    
    def __str__(self):
        return f"{self.customer.name} - {self.insurance.name} ({self.status})"
