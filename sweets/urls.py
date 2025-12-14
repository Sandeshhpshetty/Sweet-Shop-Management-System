from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SweetViewSet

router = DefaultRouter()
router.register("", SweetViewSet, basename="sweets")

urlpatterns = [
    path("", include(router.urls)),
]
