from rest_framework.decorators import action
from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import get_user_model
from product.models import Category, Product, Cart
from product.serializers import CategorySerializer, ProductSerializer, CartSerializer


User = get_user_model()

class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.select_related('category').all()

class CartViewSet(ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only return cart items for the authenticated user
        return Cart.objects.select_related('product', 'user').filter(user=self.request.user)

    # @action(detail=False, methods=['get'])
    # def total(self, request):
    #     """Calculate the total price of all products in the user's cart."""
    #     total = Cart.calculate_total(request.user)
    #     return Response({"total_price": total}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """Add a new product to the user's cart."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)  # Automatically associate the cart item with the authenticated user
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """Update an existing cart item (e.g., change product or user association)."""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """Remove a specific item from the user's cart."""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

