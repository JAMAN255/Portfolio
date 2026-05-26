"""
URL configuration for myapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from todo_app.views import TodoItemViewSet, CategoryViewSet, UserViewSet, TodoItemStatusViewSet, PriorityViewSet, UserTodoViewSet
from insuranceapp.views import InsuranceViewSet, InsCategoryViewSet as ICVS, PriceViewSet, UserViewSet as IUVS, InsuranceStatusViewSet 

router = DefaultRouter()
# Todo API endpoints
router.register(r"todo", TodoItemViewSet)
router.register(r"todo_category", CategoryViewSet)
router.register(r"todo_user", UserViewSet)
router.register(r"todo_status", TodoItemStatusViewSet)
router.register(r"priority", PriorityViewSet)
router.register(r"user_todo", UserTodoViewSet)
# Insurance API endpoints
router.register(r"insurance", InsuranceViewSet)
router.register(r"ins_category", ICVS)
router.register(r"price", PriceViewSet)
router.register(r"insurance_user", IUVS)
router.register(r"insurance_status", InsuranceStatusViewSet)

# Urlpaths
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('calculator/', include('calculator.urls')),
    path('', include('homepage.urls')),
    path('', include('todo_app.urls')),
    path('insurance/', include('insuranceapp.urls'))
]
