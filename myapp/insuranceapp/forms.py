from django import forms
from .models import Insurance, CustomerProfile, StaffProfile, CustomerInsurance
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User as DjangoUser

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column

User = get_user_model()


#Insurance creation form
class InsuranceForm(forms.ModelForm):

    class Meta:
        model = Insurance
        fields = ['name', 'description', 'ins_category', 'price', 'status']

        widgets ={
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Insurance name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Description'}),
            'ins_category': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

        labels = {
            'name': 'Insurance Name',
            'description': 'Description',
            'ins_category': 'Insurance Category',
            'price': 'Insurance Pricing',
            'status': 'Status',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='col-md-12'),
            ),
            Row(
                Column('description', css_class='col-md-12'),
            ),
            Row(
                Column('ins_category', css_class='col-md-6'),
                Column('price', css_class='col-md-6'),
            ),
            Row(
                Column('status', css_class='col-md-12'),
            ),
            Submit('submit', 'Save Insurance', css_class='btn btn-primary mt-3')
        )

#Customer creation form
class UserForm(forms.ModelForm):

    class Meta:
        model = CustomerProfile
        fields = ['name', 'email', 'user_type', 'first_name', 'last_name']

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'user_type': forms.Select(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'}),
        }

        labels = {
            'first_name': 'First Name',
            'email': 'Email',
            'user_type': 'User Type',
            'last_name': 'Last Name',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='col-md-12'),
            ),
            Row(
                Column('email', css_class='col-md-12'),
            ),
            Row(
                Column('first_name', css_class='col-md-6'),
                Column('last_name', css_class='col-md-6'),
            ),
            Row(
                Column('user_type', css_class='col-md-12'),
            ),
            Submit('submit', 'Save user profile', css_class='btn btn-primary mt-3')
        )


# Registration form
class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords don't match.")
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            # Create customer profile
            CustomerProfile.objects.create(
                user=user,
                name=f"{user.first_name} {user.last_name}",
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
                user_type='customer'
            )
        return user


# Insurance Application form
class InsuranceApplicationForm(forms.ModelForm):
    class Meta:
        model = CustomerInsurance
        fields = ['notes']
        widgets = {
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Additional notes (optional)'}),
        }
        labels = {
            'notes': 'Application Notes',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            Row(
                Column('notes', css_class='col-md-12'),
            ),
            Submit('submit', 'Submit Application', css_class='btn btn-primary mt-3')
        )

class CustomerCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = CustomerProfile
        fields = ('email',)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        customer = super().save(commit=False)
        customer.set_password(self.cleaned_data["password1"])
        if commit:
            customer.save()
        return customer
    
class CustomerChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomerProfile
        fields = ('email', 'password')
    def __init__(self, *args, **kwargs):
        super(CustomerChangeForm, self).__init__(*args, **kwargs)
        self.Meta.fields.remove('password')

