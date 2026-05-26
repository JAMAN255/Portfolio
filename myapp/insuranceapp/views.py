from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
from django.views.generic.edit import FormView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Insurance, InsCategory, InsuranceStatus, CustomerProfile, Price, CustomerInsurance
from .serializers import InsuranceSerializer, InsCategorySerializer, PriceSerializer, UserSerializer, InsuranceStatusSerializer  
from .forms import InsuranceForm, UserForm, RegistrationForm, InsuranceApplicationForm

User = get_user_model()


# ===== Public Views =====
def index(request):
    context = {"message": "Insurance App"}
    return render(request, 'index.html', context)


class RegistrationView(CreateView):
    form_class = RegistrationForm
    template_name = 'insurance_app/register.html'
    success_url = reverse_lazy('insurance_login')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Register'
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Registration successful! Please log in.')
        return response


class InsuranceLoginView(LoginView):
    template_name = 'insurance_app/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('insurance_dashboard')


class InsuranceLogoutView(LogoutView):
    next_page = reverse_lazy('insurance_login')


# ===== User Dashboard =====
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'insurance_app/dashboard.html'
    login_url = 'insurance_login'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            customer_profile = self.request.user.customer_profile
            context['customer_profile'] = customer_profile
            context['applications'] = CustomerInsurance.objects.filter(customer=customer_profile).select_related('insurance')
            context['approved_insurances'] = CustomerInsurance.objects.filter(
                customer=customer_profile, 
                status__in=['approved', 'active']
            ).select_related('insurance')
        except CustomerProfile.DoesNotExist:
            context['error'] = "Customer profile not found. Please contact support."
        return context


# ===== Insurance Management (Admin Only) =====
class IsStaffUserMixin(UserPassesTestMixin):
    login_url = 'insurance_login'
    
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser


class InsuranceListView(IsStaffUserMixin, ListView):
    model = Insurance
    template_name = 'insurance_app/insurance_list.html'
    context_object_name = 'insurance'
    paginate_by = 10


class InsuranceDetailView(IsStaffUserMixin, DetailView):
    model = Insurance
    template_name = 'insurance_app/insurance_detail.html'
    context_object_name = 'insurance'


class InsuranceCreateView(IsStaffUserMixin, CreateView):
    model = Insurance
    form_class = InsuranceForm
    template_name = 'insurance_app/insurance_form.html'
    success_url = reverse_lazy('insurance_list')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Insurance created successfully!')
        return response


class InsuranceUpdateView(IsStaffUserMixin, UpdateView):
    model = Insurance
    form_class = InsuranceForm
    template_name = 'insurance_app/insurance_form.html'
    success_url = reverse_lazy('insurance_list')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Insurance updated successfully!')
        return response


class InsuranceDeleteView(IsStaffUserMixin, DeleteView):
    model = Insurance
    template_name = 'insurance_app/insurance_confirm_delete.html'
    success_url = reverse_lazy('insurance_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Insurance deleted successfully!')
        return super().form_valid(form)



class AvailableInsurancesView(LoginRequiredMixin, ListView):
    model = Insurance
    template_name = 'insurance_app/available_insurances.html'
    context_object_name = 'insurances'
    login_url = 'insurance_login'
    paginate_by = 10
    
    def get_queryset(self):
        
        return Insurance.objects.filter(status__status='active').distinct()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            customer_profile = self.request.user.customer_profile
            context['customer_profile'] = customer_profile
            
            context['applied_insurances'] = CustomerInsurance.objects.filter(
                customer=customer_profile
            ).values_list('insurance_id', flat=True)
        except CustomerProfile.DoesNotExist:
            context['error'] = "Customer profile not found."
        return context


class ApplyForInsuranceView(LoginRequiredMixin, FormView):
    form_class = InsuranceApplicationForm
    template_name = 'insurance_app/apply_insurance.html'
    login_url = 'insurance_login'
    
    def dispatch(self, request, *args, **kwargs):
        try:
            self.insurance = Insurance.objects.get(pk=kwargs['pk'])
        except Insurance.DoesNotExist:
            messages.error(request, 'Insurance not found.')
            return redirect('available_insurances')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['insurance'] = self.insurance
        return context
    
    def form_valid(self, form):
        try:
            customer_profile = self.request.user.customer_profile
            
            
            if CustomerInsurance.objects.filter(
                customer=customer_profile, 
                insurance=self.insurance
            ).exists():
                messages.warning(self.request, 'You have already applied for this insurance.')
                return redirect('available_insurances')
            
            
            application = form.save(commit=False)
            application.customer = customer_profile
            application.insurance = self.insurance
            application.save()
            
            messages.success(self.request, 'Application submitted successfully! Please wait for admin approval.')
            return redirect('insurance_dashboard')
        
        except CustomerProfile.DoesNotExist:
            messages.error(self.request, 'Customer profile not found.')
            return redirect('available_insurances')


# ===== User Management (Admin Only) =====
class UserCreateView(IsStaffUserMixin, CreateView):
    model = CustomerProfile
    form_class = UserForm
    template_name = 'insurance_app/user_create.html'
    context_object_name = 'user'
    success_url = reverse_lazy('insurance_list')


class UserDetailView(IsStaffUserMixin, DetailView):
    model = CustomerProfile
    form_class = UserForm
    template_name = 'insurance_app/user_detail.html'
    context_object_name = 'user'


class UserUpdateView(IsStaffUserMixin, UpdateView):
    model = CustomerProfile
    form_class = UserForm
    template_name = 'insurance_app/user_create.html'
    context_object_name = 'user'
    success_url = reverse_lazy('insurance_list')


class UserDeleteView(IsStaffUserMixin, DeleteView):
    model = CustomerProfile
    template_name = 'insurance_app/user_confirm_delete.html'
    context_object_name = 'user'
    success_url = reverse_lazy('insurance_list')


# ===== REST API ViewSets =====
class InsuranceViewSet(viewsets.ModelViewSet):
    queryset = Insurance.objects.all()
    serializer_class = InsuranceSerializer
    permission_classes = [IsAuthenticated]


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
    permission_classes = [IsAuthenticated]
