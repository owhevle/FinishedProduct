from django.contrib import admin
from .models import Room, MaintenanceRequest

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'room_name', 'building', 'floor', 'status', 'request_count')
    list_filter = ('building', 'floor', 'status')
    search_fields = ('room_number', 'room_name')
    ordering = ('building', 'floor', 'room_number')

@admin.register(MaintenanceRequest)
class MaintenanceRequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'room', 'priority', 'status', 'created_at')
    list_filter = ('status', 'priority', 'created_at')
    search_fields = ('title', 'description', 'room__room_number', 'room__room_name')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')