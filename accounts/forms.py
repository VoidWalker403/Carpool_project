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


from django import forms
from .models import RideOffer
from django.utils import timezone

class RideOfferForm(forms.ModelForm):
    departure_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )

    class Meta:
        model = RideOffer
        fields = [
            'from_location',
            'to_location',
            'from_lat',
            'from_lng',
            'to_lat',
            'to_lng',
            'departure_time',
            'seats_available',
            'price_per_seat',
            'notes',
        ]
        widgets = {
            'from_lat': forms.HiddenInput(),
            'from_lng': forms.HiddenInput(),
            'to_lat': forms.HiddenInput(),
            'to_lng': forms.HiddenInput(),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_departure_time(self):
        departure_time = self.cleaned_data['departure_time']
        if departure_time < timezone.now():
            raise forms.ValidationError("Departure time cannot be in the past.")
        return departure_time