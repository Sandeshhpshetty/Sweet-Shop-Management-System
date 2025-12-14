from rest_framework import generics, permissions,viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Sweet
from .serializers import SweetSerializer
from .permissions import IsAdmin
from rest_framework.decorators import action

# Add + List
class SweetListCreate(generics.ListCreateAPIView):
    queryset = Sweet.objects.all()
    serializer_class = SweetSerializer
    permission_classes = [permissions.IsAuthenticated]   # Protected


# Update + Delete
class SweetUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sweet.objects.all()
    serializer_class = SweetSerializer

    def get_permissions(self):
        if self.request.method == "DELETE":
            return [IsAdmin()]  # Admin-only delete
        return [permissions.IsAuthenticated]


# Search
class SweetSearch(APIView):
    permission_classes = [permissions.IsAuthenticated]   # Protected

    def get(self, request):
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


# Purchase
class PurchaseSweet(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, id):
        sweet = Sweet.objects.get(id=id)
        if sweet.quantity <= 0:
            return Response({"error": "Out of stock"}, status=400)

        sweet.quantity -= 1
        sweet.save()
        return Response({"message": "Purchased"})


# Restock (Admin only)
class RestockSweet(APIView):
    permission_classes = [IsAdmin]

    def post(self, request, id):
        sweet = Sweet.objects.get(id=id)
        sweet.quantity += 1
        sweet.save()
        return Response({"message": "Restocked"})

class SweetViewSet(viewsets.ModelViewSet):
    queryset = Sweet.objects.all()
    serializer_class = SweetSerializer

    def get_permissions(self):
        if self.action == "destroy":        # DELETE
            return [IsAdmin()]              # Admin only
        if self.action == "restock":        # Custom admin route
            return [IsAdmin()]              # Admin only
        return [permissions.IsAuthenticated()]  # Other endpoints require login

    # 🔎 SEARCH ENDPOINT
    @action(detail=False, methods=["get"], url_path="search")
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

    # 🛒 PURCHASE
    @action(detail=True, methods=["post"], url_path="purchase")
    def purchase(self, request, pk=None):
        sweet = Sweet.objects.get(pk=pk)
        if sweet.quantity <= 0:
            return Response({"error": "Out of stock"}, status=400)

        sweet.quantity -= 1
        sweet.save()
        return Response({"message": "Purchased successfully"})

    # 📦 RESTOCK (Admin only)
    @action(detail=True, methods=["post"], url_path="restock")
    def restock(self, request, pk=None):
        sweet = Sweet.objects.get(pk=pk)
        sweet.quantity += 1
        sweet.save()
        return Response({"message": "Restocked successfully"})
    


    @action(detail=False, methods=["post"], url_path="search")
    def search(self, request):
        name = request.data.get("name", None)

        sweets = Sweet.objects.all()

        if name:
            sweets = sweets.filter(name__icontains=name)

        serializer = SweetSerializer(sweets, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], url_path="destock")
    def destock(self, request, pk=None):
        sweet = Sweet.objects.get(pk=pk)

        # Quantity to remove
        remove_quantity = int(request.data.get("quantity", 1))

        if sweet.quantity <= 0:
            return Response({"error": "No stock available"}, status=400)

        if remove_quantity > sweet.quantity:
            return Response({"error": "Cannot destock more than available quantity"}, status=400)

        sweet.quantity -= remove_quantity
        sweet.save()

        return Response({
            "message": "Destocked successfully",
            "remaining_quantity": sweet.quantity
        })
