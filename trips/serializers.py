from rest_framework import serializers
from .models import Trip, TripRoute
from network.models import Node
from network.graph_utils import bfs
from .models import Trip, TripRoute, CarpoolRequest, DriverOffer
from network.graph_utils import bfs, calculate_detour, calculate_fare, get_nodes_within_distance

class TripRouteSerializer(serializers.ModelSerializer):
    node_name = serializers.CharField(source='node.name', read_only=True)

    class Meta:
        model = TripRoute
        fields = ['order', 'node', 'node_name', 'visited']


class TripSerializer(serializers.ModelSerializer):
    route_nodes = TripRouteSerializer(many=True, read_only=True)
    driver_username = serializers.CharField(source='driver.username', read_only=True)
    start_node_name = serializers.CharField(source='start_node.name', read_only=True)
    end_node_name = serializers.CharField(source='end_node.name', read_only=True)
    current_node_name = serializers.CharField(source='current_node.name', read_only=True)

    class Meta:
        model = Trip
        fields = [
            'id', 'driver_username', 'start_node', 'start_node_name',
            'end_node', 'end_node_name', 'current_node', 'current_node_name',
            'max_passengers', 'status', 'route_nodes', 'created_at'
        ]
        read_only_fields = ['driver_username', 'status', 'current_node', 'route_nodes']

    def create(self, validated_data):
        start = validated_data['start_node']
        end = validated_data['end_node']

        
        path_ids = bfs(start.id, end.id)
        if not path_ids:
            raise serializers.ValidationError(
                f"No route found from '{start.name}' to '{end.name}'."
            )

        
        trip = Trip.objects.create(
            **validated_data,
            current_node=start,
            status='active'
        )

       
        nodes = Node.objects.in_bulk(path_ids)
        for order, node_id in enumerate(path_ids):
            TripRoute.objects.create(
                trip=trip,
                node=nodes[node_id],
                order=order,
                visited=(order == 0)  
            )

        return trip


class UpdateCurrentNodeSerializer(serializers.Serializer):
    node_id = serializers.IntegerField()

    def validate_node_id(self, value):
        try:
            node = Node.objects.get(id=value)
        except Node.DoesNotExist:
            raise serializers.ValidationError("Node does not exist.")
        return 
    


class DriverOfferSerializer(serializers.ModelSerializer):
    driver_username = serializers.CharField(source='trip.driver.username', read_only=True)
    detour_distance = serializers.IntegerField(read_only=True)
    fare = serializers.DecimalField(max_digits=8, decimal_places=2, read_only=True)

    class Meta:
        model = DriverOffer
        fields = ['id', 'driver_username', 'detour_nodes', 'detour_distance', 'fare', 'status']


class CarpoolRequestSerializer(serializers.ModelSerializer):
    offers = DriverOfferSerializer(many=True, read_only=True)
    passenger_username = serializers.CharField(source='passenger.username', read_only=True)
    pickup_node_name = serializers.CharField(source='pickup_node.name', read_only=True)
    destination_node_name = serializers.CharField(source='destination_node.name', read_only=True)

    class Meta:
        model = CarpoolRequest
        fields = [
            'id', 'passenger_username', 'pickup_node', 'pickup_node_name',
            'destination_node', 'destination_node_name', 'status', 'offers', 'created_at'
        ]
        read_only_fields = ['passenger_username', 'status', 'offers']

    def validate(self, data):
        if data['pickup_node'] == data['destination_node']:
            raise serializers.ValidationError("Pickup and destination cannot be the same.")
        return data