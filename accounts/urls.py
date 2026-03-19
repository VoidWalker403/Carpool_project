from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("driver/", views.driver_dashboard, name="driver_dashboard"),
    path("passenger/", views.passenger_dashboard, name="passenger_dashboard"),
    path("driver/offer-ride/", views.offer_ride, name="offer_ride"),
    path("driver/update-location/", views.update_live_location, name="update_live_location"),

]