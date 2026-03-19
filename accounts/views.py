import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import Group
from .forms import SignUpForm, RideOfferForm
from .models import RideOffer, LiveLocation
from django.shortcuts import render

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()

            role = form.cleaned_data["role"]  # "Drivers" or "Passengers"
            group, _ = Group.objects.get_or_create(name=role)
            user.groups.add(group)

            login(request, user)

            # send them to their dashboard
            if role == "Drivers":
                return redirect("/driver/")
            return redirect("/passenger/")
    else:
        form = SignUpForm()

    return render(request, "registration/signup.html", {"form": form})

@login_required
def driver_dashboard(request):
    rides = RideOffer.objects.filter(driver=request.user).order_by('-created_at')

    return render(request, "driver/dashboard.html", {
        "rides": rides
    })

@login_required
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

    return render(request, "driver/offer_ride.html", {
        "form": form
    })

@login_required
def passenger_dashboard(request):
    rides = RideOffer.objects.filter(is_active=True).order_by('-created_at')

    return render(request, "passenger/dashboard.html",{
        "rides": rides
    })

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
            defaults={
                'lat': lat,
                'lng': lng
            }
        )
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})