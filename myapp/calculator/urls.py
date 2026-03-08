from django.urls import path
from . import views

urlpatterns = [
    path('projects/calculator', views.calculator, name='calculator'),
]