from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.db import models  # Import models for aggregation
from .models import Customer, Category, Product, Order
from .serializers import UserSerializer, CustomerSerializer, CategorySerializer, ProductSerializer, OrderSerializer
from .utils import send_order_email, send_order_sms




from django.shortcuts import render
from django.http import HttpResponse
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from base.serializers import *
from django.db import IntegrityError


# Create your views here.







class AuthView(APIView):
    def post(self, request):
        # Step 1: Get the auth code from the request
        email = request.data.get('email')


        try:
            user = User.objects.get(email=email)
        except CustomUser.DoesNotExist:
            # Create new user if not exists
            try:
                user = User.objects.create(
                    email=email,
                    username=email,
                    first_name=user_info.get('given_name', ''),
                    last_name=user_info.get('family_name', ''),
                )
            except IntegrityError:
                return Response({'detail': 'Error creating user'}, status=status.HTTP_400_BAD_REQUEST)

        # Step 5: Generate tokens for the user
        refresh = RefreshToken.for_user(user)
        user_serializer = UserSerializer(user)

        # Step 6: Filter the user data and construct the response
        filtered_user_data = {
            'id': user_serializer.data['id'],
            'username': user_serializer.data['username'],
            'email': user_serializer.data['email'],
            'name': user_serializer.data['first_name'],
        }

        # Include the token field
        filtered_user_data['token'] = str(refresh.access_token)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            **filtered_user_data,
        }, status=status.HTTP_200_OK)







class RegisterAdmin(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        # Check if there is an existing admin
        existing_admin = User.objects.filter(is_staff=True).exclude(id=user.id).first()

        if user.is_staff:
            # If the user is already an admin, deregister them
            user.is_staff = False
            user.save()
            return Response({'detail': 'User deregistered as admin.'}, status=status.HTTP_200_OK)
        else:
            # If there is an existing admin, remove their admin status
            if existing_admin:
                existing_admin.is_staff = False
                existing_admin.save()

            # Register the current user as the sole admin
            user.is_staff = True
            user.save()
            return Response({'detail': 'User registered as admin.'}, status=status.HTTP_200_OK)

class CreateProduct(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # if not request.user.is_staff:
        #     return Response({'detail': 'Only admins can create products.'}, status=status.HTTP_403_FORBIDDEN)


        data = request.data.copy()
        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateOrder(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        # Ensure the user has a customer object
        if not hasattr(user, 'customer'):
            customer = Customer.objects.create(user=user, phone_number='', address='')
        else:
            customer = user.customer

        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')

        if not product_id or not quantity:
            return Response({'detail': 'Product ID and quantity are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'detail': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)

        order = Order.objects.create(customer=customer, product=product, quantity=quantity)
        send_order_email(order)
        return Response({'detail': 'Order created successfully!'}, status=status.HTTP_201_CREATED)

class AverageProductPrice(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        category_id = request.data.get('category_id')
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




class CategoryList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProductList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)