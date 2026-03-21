from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404, render
from .models import Trip, TripRoute, CarpoolRequest, DriverOffer
from .serializers import TripSerializer, UpdateCurrentNodeSerializer, CarpoolRequestSerializer, DriverOfferSerializer
from network.models import Node
from network.graph_utils import calculate_detour, calculate_fare, get_nodes_within_distance
from core.models import ServiceStatus


def check_service_active():
    """Raises ValidationError if service is suspended."""
    status_obj = ServiceStatus.get_status()
    if not status_obj.is_active:
        raise ValidationError(
            f'Carpooling service is currently suspended. Reason: {status_obj.suspended_reason}'
        )


class PublishTripView(generics.CreateAPIView):
    serializer_class = TripSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        check_service_active()  # ✅ raises error if suspended
        serializer.save(driver=self.request.user)


class MyTripsView(generics.ListAPIView):
    serializer_class = TripSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Trip.objects.filter(driver=self.request.user).order_by('-created_at')


class CancelTripView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, trip_id):
        trip = get_object_or_404(Trip, id=trip_id, driver=request.user)

        if trip.status != 'active':
            return Response(
                {'error': 'Only active trips can be cancelled.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        trip.status = 'cancelled'
        trip.save()
        return Response({'message': 'Trip cancelled successfully.'})


class UpdateCurrentNodeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, trip_id):
        trip = get_object_or_404(Trip, id=trip_id, driver=request.user)

        if trip.status not in ['active', 'in_progress']:
            return Response(
                {'error': 'Trip is not active.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = UpdateCurrentNodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        node_id = serializer.validated_data['node_id']

        route_entry = TripRoute.objects.filter(
            trip=trip, node_id=node_id, visited=False
        ).first()

        if not route_entry:
            return Response(
                {'error': 'Node is not in the route or already visited.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        TripRoute.objects.filter(
            trip=trip, order__lte=route_entry.order
        ).update(visited=True)

        trip.current_node_id = node_id
        trip.status = 'in_progress'

        if node_id == trip.end_node_id:
            trip.status = 'completed'

        trip.save()

        return Response({
            'message': f'Current node updated to {route_entry.node.name}.',
            'status': trip.status
        })


# ─── PASSENGER VIEWS ─────────────────────────────────────────

class SubmitCarpoolRequestView(generics.CreateAPIView):
    serializer_class = CarpoolRequestSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        check_service_active()  # ✅ raises error if suspended
        serializer.save(passenger=self.request.user)


class ViewOffersView(generics.RetrieveAPIView):
    serializer_class = CarpoolRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(
            CarpoolRequest,
            id=self.kwargs['request_id'],
            passenger=self.request.user
        )


class ConfirmOfferView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, request_id, offer_id):
        carpool_request = get_object_or_404(
            CarpoolRequest, id=request_id, passenger=request.user
        )
        if carpool_request.status != 'pending':
            return Response({'error': 'Request is no longer pending.'}, status=400)

        offer = get_object_or_404(DriverOffer, id=offer_id, carpool_request=carpool_request)

        DriverOffer.objects.filter(carpool_request=carpool_request).exclude(id=offer_id).update(status='rejected')
        offer.status = 'confirmed'
        offer.save()

        carpool_request.status = 'confirmed'
        carpool_request.confirmed_offer = offer
        carpool_request.save()

        return Response({'message': 'Offer confirmed successfully.'})


class CancelCarpoolRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, request_id):
        carpool_request = get_object_or_404(
            CarpoolRequest, id=request_id, passenger=request.user
        )
        if carpool_request.status == 'confirmed':
            return Response({'error': 'Cannot cancel a confirmed request.'}, status=400)

        carpool_request.status = 'cancelled'
        carpool_request.save()
        return Response({'message': 'Request cancelled.'})


# ─── DRIVER VIEWS ────────────────────────────────────────────

class IncomingRequestsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, trip_id):
        trip = get_object_or_404(Trip, id=trip_id, driver=request.user)

        remaining_nodes = list(
            TripRoute.objects.filter(trip=trip, visited=False)
            .order_by('order')
            .values_list('node_id', flat=True)
        )

        nearby_node_ids = get_nodes_within_distance(remaining_nodes, max_distance=2)

        incoming = CarpoolRequest.objects.filter(
            status='pending',
            pickup_node_id__in=nearby_node_ids,
            destination_node_id__in=nearby_node_ids
        ).select_related('passenger', 'pickup_node', 'destination_node')

        return render(request, 'trips/incoming_requests.html', {
            'trip': trip,
            'requests': incoming,
        })


class MakeOfferView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, trip_id, request_id):
        trip = get_object_or_404(Trip, id=trip_id, driver=request.user)
        carpool_request = get_object_or_404(CarpoolRequest, id=request_id, status='pending')

        if DriverOffer.objects.filter(trip=trip, carpool_request=carpool_request).exists():
            return Response({'error': 'You already made an offer for this request.'}, status=400)

        remaining_nodes = list(
            TripRoute.objects.filter(trip=trip, visited=False)
            .order_by('order')
            .values_list('node_id', flat=True)
        )

        detour_nodes, detour_distance = calculate_detour(
            remaining_nodes,
            carpool_request.pickup_node_id,
            carpool_request.destination_node_id
        )

        if detour_nodes is None:
            return Response({'error': 'Cannot serve this passenger on your route.'}, status=400)

        fare = calculate_fare(detour_nodes, trip.id)

        offer = DriverOffer.objects.create(
            trip=trip,
            carpool_request=carpool_request,
            detour_nodes=detour_nodes,
            detour_distance=detour_distance,
            fare=fare
        )

        return Response(DriverOfferSerializer(offer).data, status=201)


class DriverTripSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, trip_id):
        trip = get_object_or_404(Trip, id=trip_id, driver=request.user)
        offers = DriverOffer.objects.filter(trip=trip).select_related('carpool_request')

        return render(request, 'trips/driver_summary.html', {
            'trip': trip,
            'pending_offers': offers.filter(status='pending'),
            'confirmed_carpools': offers.filter(status='confirmed'),
            'past_requests': offers.filter(status='rejected'),
        })