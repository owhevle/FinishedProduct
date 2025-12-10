# views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Room, MaintenanceRequest
from .serializers import RoomSerializer, MaintenanceRequestSerializer

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['get'])
    def by_building_floor(self, request):
        building = request.query_params.get('building')
        floor = request.query_params.get('floor')
        
        if building and floor:
            rooms = Room.objects.filter(building=building, floor=floor)
            serializer = self.get_serializer(rooms, many=True)
            return Response(serializer.data)
        
        return Response([])

class MaintenanceRequestViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceRequest.objects.all()
    serializer_class = MaintenanceRequestSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = MaintenanceRequest.objects.all()
        room_id = self.request.query_params.get('room_id')
        
        if room_id:
            queryset = queryset.filter(room_id=room_id)
        
        return queryset
    
    def create(self, request, *args, **kwargs):
        room_id = request.data.get('room')
        
        if not room_id:
            return Response(
                {'error': 'Room ID is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Try to get the room
        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            # Room doesn't exist - we need to get its position from frontend data
            # The frontend should send room_position data when creating a request
            building = request.data.get('building', 'UNKNOWN')
            floor = request.data.get('floor', 'UNKNOWN')
            
            # Get position data if provided in the request
            x = request.data.get('x', 0)
            y = request.data.get('y', 0)
            width = request.data.get('width', 100)
            height = request.data.get('height', 100)
            
            # Create the room with position data
            room = Room.objects.create(
                id=room_id,
                room_number=room_id,
                room_name=request.data.get('room_name', f"Room {room_id}"),
                building=building,
                floor=floor,
                x=x,
                y=y,
                width=width,
                height=height,
                status='pending'
            )
        
        # Create the maintenance request
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(room=room)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)