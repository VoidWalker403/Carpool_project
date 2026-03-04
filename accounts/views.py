from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import Group
from .forms import SignUpForm

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