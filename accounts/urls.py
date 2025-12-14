from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

router = DefaultRouter()
router.register("users", UserViewSet, basename="users")

urlpatterns = [
    path('', include(router.urls)),

    # Login using JWT
    path("login/", TokenObtainPairView.as_view(), name="login"),
]
