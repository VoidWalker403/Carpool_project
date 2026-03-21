from django.contrib import admin
from django.utils.html import format_html
from .models import Trip, TripRoute, CarpoolRequest, DriverOffer


class TripRouteInline(admin.TabularInline):
    model = TripRoute
    extra = 0
    readonly_fields = ('node', 'order', 'visited')
    can_delete = False


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('id', 'driver', 'start_node', 'end_node', 'current_node', 'max_passengers', 'status_display', 'created_at')
    list_filter = ('status',)
    search_fields = ('driver__username',)
    readonly_fields = ('driver', 'start_node', 'end_node', 'current_node', 'created_at')
    inlines = [TripRouteInline]

    def status_display(self, obj):
        colors = {
            'active': 'green',
            'in_progress': 'blue',
            'completed': 'grey',
            'cancelled': 'red',
        }
        color = colors.get(obj.status, 'black')
        return format_html(
            '<span style="color:{}; font-weight:bold;">{}</span>',
            color, obj.status.upper()
        )
    status_display.short_description = "Status"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('driver', 'start_node', 'end_node', 'current_node')


@admin.register(CarpoolRequest)
class CarpoolRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'passenger', 'pickup_node', 'destination_node', 'status', 'created_at')
    list_filter = ('status',)
    readonly_fields = ('passenger', 'pickup_node', 'destination_node', 'confirmed_offer')


@admin.register(DriverOffer)
class DriverOfferAdmin(admin.ModelAdmin):
    list_display = ('id', 'trip', 'carpool_request', 'detour_distance', 'fare', 'status')
    list_filter = ('status',)
    readonly_fields = ('trip', 'carpool_request', 'detour_nodes', 'detour_distance', 'fare')