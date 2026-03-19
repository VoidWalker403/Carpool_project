from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.created_at}"
    

from django.db import models

class Node(models.Model):
    """Represents a physical location or waypoint on the road network."""
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Edge(models.Model):
    """
    Represents a directed connection between two nodes (one-way road).
    source -> destination (directed, unweighted)
    """
    source = models.ForeignKey(
        Node,
        on_delete=models.CASCADE,
        related_name='outgoing_edges'
    )
    destination = models.ForeignKey(
        Node,
        on_delete=models.CASCADE,
        related_name='incoming_edges'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.source.name} → {self.destination.name}"

    class Meta:
        unique_together = ('source', 'destination')  # no duplicate edges
        ordering = ['source__name', 'destination__name']