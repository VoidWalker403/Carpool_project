from django.urls import path
from .views import PublishTripView, MyTripsView, CancelTripView, UpdateCurrentNodeView

urlpatterns = [
    path('publish/', PublishTripView.as_view(), name='publish_trip'),
    path('my-trips/', MyTripsView.as_view(), name='my_trips'),
    path('<int:trip_id>/cancel/', CancelTripView.as_view(), name='cancel_trip'),
    path('<int:trip_id>/update-node/', UpdateCurrentNodeView.as_view(), name='update_current_node'),
]