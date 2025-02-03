from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Customer, Category, Product, Order
from .serializers import UserSerializer, CustomerSerializer, CategorySerializer, ProductSerializer, OrderSerializer
from .utils import send_order_email, send_order_sms
from django.db import models


class RegisterAdmin(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_staff = True
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateProduct(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not request.user.is_staff:
            return Response({'detail': 'Only admins can create products.'}, status=status.HTTP_403_FORBIDDEN)
        data = request.data.copy()
        data['admin'] = request.user.id
        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateOrder(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()
            send_order_email(order)
            send_order_sms(order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AverageProductPrice(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)
        products = category.products.all()
        if not products:
            return Response({'detail': 'No products found in this category'}, status=status.HTTP_404_NOT_FOUND)
        average_price = products.aggregate(models.Avg('price'))['price__avg']
        return Response({'average_price': average_price}, status=status.HTTP_200_OK)
    







class CreateCategory(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)