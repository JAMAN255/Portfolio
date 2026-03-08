from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='Home'),
    path('contact/', views.contact, name='Contact'),
    path('projects/', views.projects, name='Projects'),
]