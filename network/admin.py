from django.contrib import admin
from .models import Post

admin.site.register(Post)

from django.contrib import admin
from .models import Node, Edge

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