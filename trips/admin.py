from django.contrib import admin
from .models import Trip, TripRoute

class TripRouteInline(admin.TabularInline):
    model = TripRoute
    extra = 0
    readonly_fields = ('node', 'order', 'visited')

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('id', 'driver', 'start_node', 'end_node', 'current_node', 'max_passengers', 'status', 'created_at')
    list_filter = ('status',)
    inlines = [TripRouteInline]