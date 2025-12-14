from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser


from .models import Sweet
from .serializers import SweetSerializer


class SweetViewSet(viewsets.ModelViewSet):
    queryset = Sweet.objects.all()
    serializer_class = SweetSerializer
    permission_classes = [IsAuthenticated]   # login required for all actions

    @action(
        detail=True,
        methods=["post"],
        url_path="restock",
        permission_classes=[IsAdminUser]    # 🔥 ONLY ADMIN CAN RESTORE
    )
    def restock(self, request, pk=None):
        sweet = get_object_or_404(Sweet, pk=pk)
        sweet.quantity += 1
        sweet.save()
        return Response({"message": "Restocked successfully"})



    # LIST OVERRIDE (OPTIONAL)
    def list(self, request, *args, **kwargs):
        queryset = Sweet.objects.all()
        serializer = SweetSerializer(queryset, many=True)
        return Response(serializer.data)

    # SEARCH
    @action(detail=False, methods=["get"], url_path="search", permission_classes=[AllowAny])
    def search(self, request):
        name = request.GET.get("name")
        category = request.GET.get("category")
        min_price = request.GET.get("min")
        max_price = request.GET.get("max")

        sweets = Sweet.objects.all()

        if name:
            sweets = sweets.filter(name__icontains=name)
        if category:
            sweets = sweets.filter(category__icontains=category)
        if min_price and max_price:
            sweets = sweets.filter(price__gte=min_price, price__lte=max_price)

        serializer = SweetSerializer(sweets, many=True)
        return Response(serializer.data)

    # PURCHASE
    @action(detail=True, methods=["post"], url_path="purchase", permission_classes=[AllowAny])
    def purchase(self, request, pk=None):
        sweet = get_object_or_404(Sweet, pk=pk)

        if sweet.quantity <= 0:
            return Response({"error": "Out of stock"}, status=400)

        sweet.quantity -= 1
        sweet.save()
        return Response({"message": "Purchased successfully"})

    # RESTOCK
    @action(detail=True, methods=["post"], url_path="restock", permission_classes=[AllowAny])
    def restock(self, request, pk=None):
        sweet = get_object_or_404(Sweet, pk=pk)
        sweet.quantity += 1
        sweet.save()
        return Response({"message": "Restocked successfully"})
