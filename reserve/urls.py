from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ReserveViewSet

router = DefaultRouter()
router.register('reservations', ReserveViewSet)

urlpatterns = [
    path('', include(router.urls))
]