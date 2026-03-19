from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)


    class Meta:
        model = Post
        fields = ['id', 'content', 'created_at', 'user']
        read_only_fields = ['user']

from rest_framework import serializers
from .models import Node, Edge

class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = ['id', 'name', 'description', 'latitude', 'longitude']


class EdgeSerializer(serializers.ModelSerializer):
    source_name = serializers.CharField(source='source.name', read_only=True)
    destination_name = serializers.CharField(source='destination.name', read_only=True)

    class Meta:
        model = Edge
        fields = ['id', 'source', 'source_name', 'destination', 'destination_name']

    def validate(self, data):
        if data['source'] == data['destination']:
            raise serializers.ValidationError("Source and destination cannot be the same node.")
        return data