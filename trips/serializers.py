from rest_framework import serializers
from .models import Trip, TripRoute
from network.models import Node
from network.graph_utils import bfs

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
        return value