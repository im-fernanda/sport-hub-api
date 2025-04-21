from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import *

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"time_slots", TimeSlotViewSet, basename="time_slot")
router.register(r"spaces", SpaceViewSet, basename="space")
router.register(r"reservations", ReservationViewSet, basename="reservation")


urlpatterns = [path("", include(router.urls))]
