from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'rooms', views.RoomViewSet)
router.register(r'requests', views.MaintenanceRequestViewSet)

urlpatterns = [
    path('', include(router.urls)),
]