from django.contrib.auth import login
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect

from .forms import SignUpForm

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Default role: Passenger
            passengers, _ = Group.objects.get_or_create(name="Passengers")
            user.groups.add(passengers)

            login(request, user)  # auto-login after signup
            return redirect("/passenger/")
    else:
        form = SignUpForm()

    return render(request, "registration/signup.html", {"form": form})