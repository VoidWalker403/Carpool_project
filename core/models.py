from django.db import models

class ServiceStatus(models.Model):
    """Singleton model to control whether carpooling is enabled or suspended."""
    is_active = models.BooleanField(default=True)
    suspended_reason = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Service Status"
        verbose_name_plural = "Service Status"

    def __str__(self):
        return "Service Active" if self.is_active else f"Service Suspended: {self.suspended_reason}"

    @classmethod
    def get_status(cls):
        """Always returns the single instance, creates it if it doesn't exist."""
        obj, _ = cls.objects.get_or_create(id=1)
        return obj