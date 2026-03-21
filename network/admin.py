from django.contrib import admin
from .models import Post

admin.site.register(Post)

from django.contrib import admin
from .models import Node, Edge

from django.utils.html import format_html
@admin.register(Node)
class NodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'latitude', 'longitude', 'created_at')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Edge)
class EdgeAdmin(admin.ModelAdmin):
    list_display = ('id', 'source', 'destination', 'created_at')
    search_fields = ('source__name', 'destination__name')
    list_filter = ('source', 'destination')
    autocomplete_fields = ('source', 'destination')



@admin.register(Node)
class NodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'latitude', 'longitude', 'created_at')
    search_fields = ('name',)
    ordering = ('name',)

    def get_outgoing_edges(self, obj):
        edges = obj.outgoing_edges.all()
        return ", ".join([str(e.destination.name) for e in edges]) or "None"
    get_outgoing_edges.short_description = "Connects To"

    list_display = ('id', 'name', 'description', 'get_outgoing_edges', 'created_at')


@admin.register(Edge)
class EdgeAdmin(admin.ModelAdmin):
    list_display = ('id', 'source', 'arrow', 'destination', 'created_at')
    search_fields = ('source__name', 'destination__name')
    autocomplete_fields = ('source', 'destination')

    def arrow(self, obj):
        return format_html('→')
    arrow.short_description = ''