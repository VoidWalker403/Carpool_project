from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    ROLE_CHOICES = (
        ("Passengers", "Passenger (find rides)"),
        ("Drivers", "Driver (offer rides)"),
    )
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = ("username", "email", "role", "password1", "password2")