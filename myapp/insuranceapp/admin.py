from django.contrib import admin

# Register your models here.

from .models import Insurance, CustomerProfile, StaffProfile

admin.site.register(CustomerProfile)
admin.site.register(StaffProfile)
admin.site.register(Insurance)
