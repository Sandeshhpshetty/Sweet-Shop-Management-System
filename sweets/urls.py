from django.urls import path
from .views import (
    SweetListCreate,
    SweetUpdateDelete,
    SweetSearch,
    PurchaseSweet,
    RestockSweet
)

urlpatterns = [
    path("", SweetListCreate.as_view()),
    path("search/", SweetSearch.as_view()),
    path("<int:pk>/", SweetUpdateDelete.as_view()),
    path("<int:id>/purchase/", PurchaseSweet.as_view()),
    path("<int:id>/restock/", RestockSweet.as_view()),
]

from rest_framework.routers import DefaultRouter
from .views import SweetViewSet

router = DefaultRouter()
router.register("", SweetViewSet, basename="sweets")

urlpatterns = router.urls

