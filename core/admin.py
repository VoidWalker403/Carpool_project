from django.contrib import admin
from django.utils.html import format_html
from .models import ServiceStatus

@admin.register(ServiceStatus)
class ServiceStatusAdmin(admin.ModelAdmin):
    list_display = ('status_display', 'suspended_reason', 'updated_at')
    fields = ('is_active', 'suspended_reason')

    def status_display(self, obj):
        if obj.is_active:
            return format_html('<span style="color:green; font-weight:bold;">✅ Active</span>')
        return format_html('<span style="color:red; font-weight:bold;">🚫 Suspended</span>')
    status_display.short_description = "Service Status"

    def has_add_permission(self, request):
        # Only allow one instance
        return not ServiceStatus.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False