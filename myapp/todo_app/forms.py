from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column
from todo_app.models import TodoItem, Category, TodoItemStatus, Priority
from django.contrib.auth import get_user_model

User = get_user_model()


class TodoItemForm(forms.ModelForm):
    class Meta:
        model = TodoItem
        fields = ['name', 'description', 'category', 'user', 'status', 'priority', 'due_date']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Task name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Description'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'user': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        labels = {
            'name': 'Task Name',
            'description': 'Description',
            'category': 'Category',
            'user': 'Assigned User',
            'status': 'Status',
            'priority': 'Priority (1-10)',
            'due_date': 'Due Date',
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
                Column('category', css_class='col-md-6'),
                Column('user', css_class='col-md-6'),
            ),
            Row(
                Column('status', css_class='col-md-4'),
                Column('priority', css_class='col-md-4'),
                Column('due_date', css_class='col-md-4'),
            ),
            Submit('submit', 'Save Task', css_class='btn btn-primary mt-3')
        )


