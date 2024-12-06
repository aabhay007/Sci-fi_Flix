from django.contrib import admin
from .models import Category, Movie, User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

admin.site.register(Category)
admin.site.register(Movie)
# admin.site.register(User)

class UserAdmin(BaseUserAdmin):
    # Define the fields to be displayed in the admin list view
    list_display = ('email', 'phone_number', 'is_active', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('email', 'phone_number')
    ordering = ('email',)

    # Define the fields to be displayed and edited in the admin detail view
    fieldsets = (
        (None, {'fields': ('email', 'phone_number', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    
    # Fields used when creating a new user in the admin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone_number', 'password1', 'password2'),
        }),
    )

admin.site.register(User, UserAdmin)