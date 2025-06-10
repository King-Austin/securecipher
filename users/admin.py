from django.contrib import admin
from .models import SecureCipherUser


@admin.register(SecureCipherUser)
class SecureCipherUserAdmin(admin.ModelAdmin):
    # What it does: Displays these fields in the admin list view
    list_display = ['username', 'full_name', 'email', 'virtual_account_id', 'registered_at']
    
    # What it does: Makes these fields clickable links to the detail view
    list_display_links = ['username', 'full_name']
    
    # What it does: Adds search functionality for these fields
    search_fields = ['username', 'email', 'phone_number', 'virtual_account_id']
    
    # What it does: Adds filter options in the right sidebar
    list_filter = ['registered_at']
    
    # What it does: Shows these fields as read-only in the edit form
    readonly_fields = ['virtual_account_id', 'registered_at']
    
    # What it does: Orders the list by registration date (newest first)
    ordering = ['-registered_at']
    
    # What it does: Organizes fields into sections in the edit form
    fieldsets = (
        ('User Information', {
            'fields': ('username', 'full_name', 'email')
        }),
        ('Contact & Identity', {
            'fields': ('phone_number', 'bvn', 'nin')
        }),
        ('Security', {
            'fields': ('ecdsa_public_key',)
        }),
        ('System Generated', {
            'fields': ('virtual_account_id', 'registered_at'),
            'classes': ('collapse',)
        }),
    )
