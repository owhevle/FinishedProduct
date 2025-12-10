# models.py
from django.db import models

class Room(models.Model):
    STATUS_CHOICES = [
        ('no_request', 'No Request'),
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    
    id = models.CharField(max_length=100, primary_key=True)
    room_number = models.CharField(max_length=50)
    room_name = models.CharField(max_length=200)
    building = models.CharField(max_length=100)
    floor = models.CharField(max_length=100)
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    width = models.IntegerField(default=100)
    height = models.IntegerField(default=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='no_request')
    request_count = models.IntegerField(default=0)
    special = models.CharField(max_length=50, blank=True, null=True)
    
    class Meta:
        ordering = ['building', 'floor', 'room_number']
    
    def __str__(self):
        return f"{self.room_number} - {self.room_name} ({self.building} {self.floor})"

class MaintenanceRequest(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='requests')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.room.room_number}"
    
    def save(self, *args, **kwargs):
        is_new = not self.pk
        
        # First save the request
        super().save(*args, **kwargs)
        
        # Then update room status
        if is_new:  # New request
            self.room.request_count += 1
            self.room.status = 'pending'
            self.room.save()
        else:  # Existing request - update room status based on all requests
            pending_requests = MaintenanceRequest.objects.filter(
                room=self.room, 
                status__in=['pending', 'in_progress']
            )
            
            if pending_requests.exists():
                # Check if any are in progress
                in_progress = pending_requests.filter(status='in_progress').exists()
                if in_progress:
                    self.room.status = 'in_progress'
                else:
                    self.room.status = 'pending'
            else:
                # All requests are completed
                self.room.status = 'completed'
            
            self.room.save()