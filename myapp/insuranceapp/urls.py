from django.urls import path
from . import views


urlpatterns = [
    # Authentication URLs
    path('register/', views.RegistrationView.as_view(), name='insurance_register'),
    path('login/', views.InsuranceLoginView.as_view(), name='insurance_login'),
    path('logout/', views.InsuranceLogoutView.as_view(), name='insurance_logout'),
    
    # Customer Dashboard & Applications
    path('dashboard/', views.DashboardView.as_view(), name='insurance_dashboard'),
    path('available-insurances/', views.AvailableInsurancesView.as_view(), name='available_insurances'),
    path('apply/<int:pk>/', views.ApplyForInsuranceView.as_view(), name='apply_insurance'),
    
    # Admin Insurance Management
    path('list/', views.InsuranceListView.as_view(), name='insurance_list'),
    path('<int:pk>/', views.InsuranceDetailView.as_view(), name='insurance_detail'),
    path('create/', views.InsuranceCreateView.as_view(), name='insurance_form'),
    path('<int:pk>/update/', views.InsuranceUpdateView.as_view(), name='insurance_update'),  
    path('<int:pk>/delete/', views.InsuranceDeleteView.as_view(), name='insurance_confirm_delete'),
]