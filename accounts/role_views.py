from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse

@login_required
def passenger_dashboard(request):
    return render(request, "passenger/dashboard.html")

@login_required
def driver_dashboard(request):
    return HttpResponse("✅ Driver Dashboard: Publish/manage trips (coming next)")