from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Trip, TripRoute
from .serializers import TripSerializer, UpdateCurrentNodeSerializer
from network.models import Node

class PublishTripView(generics.CreateAPIView):
    
    serializer_class = TripSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
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
