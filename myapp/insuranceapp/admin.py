from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model

# Register your models here.

from .models import InsCategory, Insurance, CustomerProfile, InsuranceStatus, Price, StaffProfile, CustomerInsurance

User = get_user_model()


class CustomerProfileInline(admin.StackedInline):
    model = CustomerProfile
    can_delete = False
    fields = ('policy_number', 'date_of_birth', 'first_name', 'last_name', 'user_type')


class UserAdmin(BaseUserAdmin):
    inlines = (CustomerProfileInline,)
    ordering = ('email',)
    list_display = ('email', 'first_name', 'last_name', 'is_staff')


class CustomerInsuranceInline(admin.TabularInline):
    model = CustomerInsurance
    extra = 1
    fields = ('insurance', 'status', 'applied_at', 'approved_at', 'notes')
    readonly_fields = ('applied_at', 'approved_at')


class CustomerProfileAdmin(admin.ModelAdmin):
    inlines = [CustomerInsuranceInline]
    list_display = ('name', 'email', 'user_type', 'policy_number')
    search_fields = ('name', 'email', 'policy_number')
    list_filter = ('user_type',)


class InsuranceAdmin(admin.ModelAdmin):
    list_display = ('name', 'ins_category', 'price', 'status')
    search_fields = ('name', 'description')
    list_filter = ('ins_category', 'status')


class CustomerInsuranceAdmin(admin.ModelAdmin):
    list_display = ('customer', 'insurance', 'status', 'applied_at', 'approved_at')
    search_fields = ('customer__name', 'insurance__name')
    list_filter = ('status', 'applied_at')
    readonly_fields = ('applied_at',)
    actions = ['approve_applications', 'reject_applications']
    
    def approve_applications(self, request, queryset):
        from django.utils import timezone
        updated = queryset.filter(status='pending').update(status='approved', approved_at=timezone.now())
        self.message_user(request, f'{updated} application(s) approved.')
    approve_applications.short_description = "Approve selected applications"
    
    def reject_applications(self, request, queryset):
        updated = queryset.filter(status='pending').update(status='rejected')
        self.message_user(request, f'{updated} application(s) rejected.')
    reject_applications.short_description = "Reject selected applications"


# Unregister default User admin
admin.site.unregister(User)

# Register with custom admin
admin.site.register(User, UserAdmin)
admin.site.register(CustomerProfile, CustomerProfileAdmin)
admin.site.register(StaffProfile)
admin.site.register(Insurance, InsuranceAdmin)
admin.site.register(InsuranceStatus)
admin.site.register(Price)
admin.site.register(InsCategory)
admin.site.register(CustomerInsurance, CustomerInsuranceAdmin)
