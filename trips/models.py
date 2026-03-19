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

class CarpoolRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    passenger = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='carpool_requests'
    )
    pickup_node = models.ForeignKey(
        Node, on_delete=models.CASCADE, related_name='pickup_requests'
    )
    destination_node = models.ForeignKey(
        Node, on_delete=models.CASCADE, related_name='destination_requests'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    confirmed_offer = models.OneToOneField(
        'DriverOffer', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='confirmed_for_request'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request by {self.passenger} | {self.pickup_node} → {self.destination_node} [{self.status}]"


class DriverOffer(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('rejected', 'Rejected'),
    ]

    trip = models.ForeignKey(
        Trip, on_delete=models.CASCADE, related_name='driver_offers'
    )
    carpool_request = models.ForeignKey(
        CarpoolRequest, on_delete=models.CASCADE, related_name='offers'
    )
    detour_nodes = models.JSONField(default=list)   # ordered list of extra node IDs
    detour_distance = models.IntegerField(default=0)  # number of extra nodes
    fare = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Offer by {self.trip.driver} for request {self.carpool_request.id} [{self.status}]"