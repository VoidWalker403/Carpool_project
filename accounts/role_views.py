from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required
def passenger_dashboard(request):
    return HttpResponse("✅ Passenger Dashboard: Search trips + request rides (coming next)")

@login_required
def driver_dashboard(request):
    return HttpResponse("✅ Driver Dashboard: Publish/manage trips (coming next)")