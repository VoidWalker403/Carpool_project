from django.db import models
from django.conf import settings
from network.models import Node

class Trip(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    driver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='trips'
    )
    start_node = models.ForeignKey(
        Node, on_delete=models.CASCADE, related_name='trips_starting_here'
    )
    end_node = models.ForeignKey(
        Node, on_delete=models.CASCADE, related_name='trips_ending_here'
    )
    current_node = models.ForeignKey(
        Node, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='driver_currently_here'
    )
    max_passengers = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Trip by {self.driver} | {self.start_node} → {self.end_node} [{self.status}]"


class TripRoute(models.Model):
    
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='route_nodes')
    node = models.ForeignKey(Node, on_delete=models.CASCADE)
    order = models.PositiveIntegerField() 
    visited = models.BooleanField(default=False) 

    class Meta:
        ordering = ['order']
        unique_together = ('trip', 'order')

    def __str__(self):
        return f"Trip {self.trip.id} | Step {self.order}: {self.node.name} ({'visited' if self.visited else 'pending'})"
