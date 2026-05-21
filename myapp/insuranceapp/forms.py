from django import forms
from .models import Insurance, CustomerProfile, StaffProfile
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column



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

