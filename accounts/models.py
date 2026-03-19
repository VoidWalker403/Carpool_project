from django.db import models
from django.contrib.auth.models import User

class RideOffer(models.Model):
    driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ride_offers')
    from_location = models.CharField(max_length=255)
    to_location = models.CharField(max_length=255)

    from_lat = models.FloatField(null=True, blank=True)
    from_lng = models.FloatField(null=True, blank=True)
    to_lat = models.FloatField(null=True, blank=True)
    to_lng = models.FloatField(null=True, blank=True)

    departure_time = models.DateTimeField()
    seats_available = models.PositiveIntegerField(default=1)
    price_per_seat = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    notes = models.TextField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.driver.username}: {self.from_location} -> {self.to_location}"


class LiveLocation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='live_location')
    lat = models.FloatField()
    lng = models.FloatField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} @ ({self.lat}, {self.lng})"
