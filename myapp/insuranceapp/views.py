from django.urls import reverse_lazy
from django.shortcuts import render
from rest_framework import viewsets, filters as f
from .models import Insurance, InsCategory, InsuranceStatus, CustomerProfile, Price
from .serializers import InsuranceSerializer, InsCategorySerializer, PriceSerializer, UserSerializer, InsuranceStatusSerializer  
from .forms import InsuranceForm, UserForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from django.contrib.auth import get_user_model
User = get_user_model()
# Create your views here.
def index(request):
    context = {"message": "Insurance App"}
    return render(request, 'index.html', context)

class InsuranceListView(ListView):
    model = Insurance
    template_name = 'insurance_app/insurance_list.html'
    context_object_name = 'insurance'

class InsuranceDetailView(DetailView):
    model = Insurance
    template_name = 'insurance_app/insurance_detail.html'
    context_object_name = 'insurance'

class InsuranceCreateView(CreateView):
    model = Insurance
    form_class = InsuranceForm
    template_name = 'insurance_app/insurance_form.html'
    success_url = reverse_lazy('insurance_list')

class InsuranceUpdateView(UpdateView):
    model = Insurance
    form_class = InsuranceForm
    template_name = 'insurance_app/insurance_form.html'
    success_url = reverse_lazy('insurance_list')

class InsuranceDeleteView(DeleteView):
    model = Insurance
    template_name = 'insurance_app/insurance_confirm_delete.html'
    success_url = reverse_lazy('insurance_list')

class UserCreateView(CreateView):
    model = CustomerProfile
    form_class = UserForm
    template_name = 'insurance_app/user_create.html'
    context_object_name = 'user'

class UserDetailView(CreateView):
    model = CustomerProfile
    form_class = UserForm
    template_name = 'insurance_app/user_detail.html'
    context_object_name = 'user'
class UserUpdateView(CreateView):
    model = CustomerProfile
    form_class = UserForm
    template_name = 'insurance_app/user_create.html'
    context_object_name = 'user'
class UserDeleteView(CreateView):
    model = CustomerProfile
    form_class = UserForm
    template_name = 'insurance_app/user_confirm_delete.html'
    context_object_name = 'user'


#REST API ViewSets

class InsuranceViewSet(viewsets.ModelViewSet):
    queryset = Insurance.objects.all()
    serializer_class = InsuranceSerializer


class InsCategoryViewSet(viewsets.ModelViewSet):
    queryset = InsCategory.objects.all()
    serializer_class = InsCategorySerializer

class PriceViewSet(viewsets.ModelViewSet):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer

class InsuranceStatusViewSet(viewsets.ModelViewSet):
    queryset = InsuranceStatus.objects.all()
    serializer_class = InsuranceStatusSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomerProfile.objects.all()
    serializer_class = UserSerializer
    serializer_class = InsuranceSerializer

class InsuranceStatusViewSet(viewsets.ModelViewSet):
    queryset = InsuranceStatus.objects.all()
    serializer_class = InsuranceStatusSerializer


