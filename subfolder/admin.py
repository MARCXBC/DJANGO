from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class CustomUserAdmin(BaseUserAdmin):
    ordering = ('email',)
    list_display = ('email', 'first_name', 'last_name', 'is_verified', 'is_staff')
    list_display_links = ('email',)
    
    # This line completely removes the built-in filters searching for username
    list_filter = ('is_verified', 'is_staff')

    # This clears out the default field sections that require a username field
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'otp', 'is_verified')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('toggle',),
            'fields': ('email', 'first_name', 'last_name', 'password'),
        }),
    )
    search_fields = ('email',)

# Register your custom class instead of the default one
admin.site.register(User, CustomUserAdmin)
