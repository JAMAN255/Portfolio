from django.urls import path
from . import views

urlpatterns = [
    path('', views.calculator, name='calculator'),
    path('index_calculator/', views.index_calculator, name='index_calculator'),
]