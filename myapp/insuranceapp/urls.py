from django.urls import path
from . import views


urlpatterns = [
    path('insurance/', views.InsuranceListView.as_view(), name='insurance_list'),
    path('insurance/<int:pk>/', views.InsuranceDetailView.as_view(), name='insurance-detail'),
    path('insurance/create/', views.InsuranceCreateView.as_view(), name='insurance_form'),
    path('insurance/<int:pk>/update/', views.InsuranceUpdateView.as_view(), name='insurance_update'),  
    path('insurance/<int:pk>/delete/', views.InsuranceDeleteView.as_view(), name='insurance_delete'),
]