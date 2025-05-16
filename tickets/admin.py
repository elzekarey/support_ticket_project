from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Ticket, Customer

# Adding user role info to django admin users
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (('Role Info', {'fields': ('is_agent','is_admin')}),)
    list_display = ('username', 'email', 'is_agent', 'is_admin', 'is_staff')

# Registering models
admin.site.register(User, UserAdmin)
admin.site.register(Ticket)
admin.site.register(Customer)
