from django.contrib import admin
from .models import Member

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    """
    Admin interface for Member model
    """
    list_display = [
        'name', 'role', 'area', 'phone', 
        'email', 'is_active', 'joined_date'
    ]
    list_filter = ['role', 'area', 'is_active', 'joined_date']
    search_fields = ['name', 'phone', 'email', 'area', 'bio']
    list_editable = ['is_active']
    list_per_page = 20
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'role', 'area', 'image')
        }),
        ('Contact Information', {
            'fields': ('phone', 'email')
        }),
        ('Additional Information', {
            'fields': ('bio', 'is_active')
        }),
        ('Metadata', {
            'fields': ('joined_date', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['joined_date', 'created_at', 'updated_at']
    
    ordering = ['role', 'name']
    
    actions = ['activate_members', 'deactivate_members']
    
    def activate_members(self, request, queryset):
        """Bulk activate members"""
        count = queryset.update(is_active=True)
        self.message_user(request, f'{count} members activated successfully.')
    activate_members.short_description = 'Activate selected members'
    
    def deactivate_members(self, request, queryset):
        """Bulk deactivate members"""
        count = queryset.update(is_active=False)
        self.message_user(request, f'{count} members deactivated successfully.')
    deactivate_members.short_description = 'Deactivate selected members'
