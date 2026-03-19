from django.urls import path
from .views import (
    PublishTripView, MyTripsView, CancelTripView, UpdateCurrentNodeView,
    SubmitCarpoolRequestView, ViewOffersView, ConfirmOfferView,
    CancelCarpoolRequestView, IncomingRequestsView, MakeOfferView,
    DriverTripSummaryView
)

urlpatterns = [
    # ── Trip Management ──
    path('publish/', PublishTripView.as_view(), name='publish_trip'),
    path('my-trips/', MyTripsView.as_view(), name='my_trips'),
    path('<int:trip_id>/cancel/', CancelTripView.as_view(), name='cancel_trip'),
    path('<int:trip_id>/update-node/', UpdateCurrentNodeView.as_view(), name='update_current_node'),

    # ── Passenger ──
    path('requests/submit/', SubmitCarpoolRequestView.as_view(), name='submit_request'),
    path('requests/<int:request_id>/offers/', ViewOffersView.as_view(), name='view_offers'),
    path('requests/<int:request_id>/confirm/<int:offer_id>/', ConfirmOfferView.as_view(), name='confirm_offer'),
    path('requests/<int:request_id>/cancel/', CancelCarpoolRequestView.as_view(), name='cancel_request'),

    # ── Driver ──
    path('<int:trip_id>/incoming-requests/', IncomingRequestsView.as_view(), name='incoming_requests'),
    path('<int:trip_id>/make-offer/<int:request_id>/', MakeOfferView.as_view(), name='make_offer'),
    path('<int:trip_id>/summary/', DriverTripSummaryView.as_view(), name='driver_summary'),
]