import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import Group
from .forms import SignUpForm, RideOfferForm
from .models import RideOffer, LiveLocation
from .decorators import driver_required, passenger_required
from trips.models import Trip


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data["role"]
            group, _ = Group.objects.get_or_create(name=role)
            user.groups.add(group)
            login(request, user)
            if role == "Drivers":
                return redirect("/driver/")
            return redirect("/passenger/")
    else:
        form = SignUpForm()
    return render(request, "registration/signup.html", {"form": form})


@login_required
@passenger_required
def passenger_dashboard(request):
    # Fetch real active trips from DB
    trips = Trip.objects.filter(
        status__in=['active', 'in_progress']
    ).select_related('driver', 'start_node', 'end_node').order_by('-created_at')

    return render(request, "passenger/dashboard.html", {
        "trips": trips
    })


@login_required
@driver_required
def driver_dashboard(request):
    # Driver's own trips
    trips = Trip.objects.filter(
        driver=request.user
    ).order_by('-created_at')

    return render(request, "driver/dashboard.html", {
        "trips": trips
    })


@login_required
@driver_required
def offer_ride(request):
    if request.method == "POST":
        form = RideOfferForm(request.POST)
        if form.is_valid():
            ride = form.save(commit=False)
            ride.driver = request.user
            ride.save()
            return redirect("/driver/")
    else:
        form = RideOfferForm()
    return render(request, "driver/offer_ride.html", {"form": form})


@login_required
@require_POST
def update_live_location(request):
    try:
        data = json.loads(request.body)
        lat = data.get('lat')
        lng = data.get('lng')
        if lat is None or lng is None:
            return JsonResponse({'success': False, 'error': 'Latitude and longitude required'})
        LiveLocation.objects.update_or_create(
            user=request.user,
            defaults={'lat': lat, 'lng': lng}
        )
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})