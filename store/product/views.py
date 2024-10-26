from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import get_user_model
from product.models import Category, Product
from product.serializers import CategorySerializer, ProductSerializer

User = get_user_model()

class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.select_related('category').all()