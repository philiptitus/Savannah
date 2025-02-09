from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Category, Product, Order, Customer

class APITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_user(username='admin', password='adminpass', email='admin@example.com', is_superuser=True)
        self.customer_user = User.objects.create_user(username='customer', password='customerpass', email='customer@example.com')
        self.customer = Customer.objects.create(user=self.customer_user, phone_number='1234567890', address='123 Street')
        self.category = Category.objects.create(name='Bakery')
        self.product = Product.objects.create(name='Bread', description='Fresh bread', price=1.99, category=self.category)
        self.order = Order.objects.create(customer=self.customer, product=self.product, quantity=2, phone_number='1234567890')

    def authenticate(self, email):
        response = self.client.post('/auth-view/', {'email': email}, format='json')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access'])

    def test_register_admin(self):
        self.authenticate('admin@example.com')
        url = reverse('register-admin')
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(User.objects.filter(username='admin', is_superuser=True).exists())

    def test_create_product(self):
        self.authenticate('admin@example.com')
        url = reverse('create-product')
        data = {'name': 'Cookies', 'description': 'Chocolate cookies', 'price': 2.99, 'category': self.category.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Product.objects.filter(name='Cookies').exists())

    def test_create_order(self):
        self.authenticate('customer@example.com')
        url = reverse('create-order')
        data = {'product_id': self.product.id, 'quantity': 3, 'phone_number': '+25476676676'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Order.objects.filter(customer=self.customer, product=self.product, quantity=3, phone_number='1234567890').exists())

    def test_average_product_price(self):
        self.authenticate('customer@example.com')
        url = reverse('average-product-price')
        data = {'category_id': self.category.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('average_price', response.data)

    def test_create_category(self):
        self.authenticate('admin@example.com')
        url = reverse('create-category')
        data = {'name': 'Produce'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Category.objects.filter(name='Produce').exists())
