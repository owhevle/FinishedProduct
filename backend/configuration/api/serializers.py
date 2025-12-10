# serializers.py
from rest_framework import serializers
from .models import Room, MaintenanceRequest

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

class MaintenanceRequestSerializer(serializers.ModelSerializer):
    room_details = serializers.SerializerMethodField()
    
    class Meta:
        model = MaintenanceRequest
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
    
    def get_room_details(self, obj):
        if obj.room:
            return {
                'id': obj.room.id,
                'room_number': obj.room.room_number,
                'room_name': obj.room.room_name,
                'building': obj.room.building,
                'floor': obj.room.floor
            }
        return None