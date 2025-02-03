from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Category, Product, Order, Customer

class APITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_user(username='admin', password='adminpass', email='admin@example.com', is_staff=True)
        self.customer_user = User.objects.create_user(username='customer', password='customerpass', email='customer@example.com')
        self.customer = Customer.objects.create(user=self.customer_user, phone_number='1234567890', address='123 Street')
        self.category = Category.objects.create(name='Bakery')
        self.product = Product.objects.create(name='Bread', description='Fresh bread', price=1.99, category=self.category, admin=self.admin_user)
        self.order = Order.objects.create(customer=self.customer, product=self.product, quantity=2)

    def test_register_admin(self):
        url = reverse('register-admin')
        data = {'username': 'newadmin', 'password': 'newadminpass', 'email': 'newadmin@example.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newadmin').exists())

    def test_create_product(self):
        self.client.login(username='admin', password='adminpass')
        url = reverse('create-product')
        data = {'name': 'Cookies', 'description': 'Chocolate cookies', 'price': 2.99, 'category': self.category.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Product.objects.filter(name='Cookies').exists())

    def test_create_order(self):
        self.client.login(username='customer', password='customerpass')
        url = reverse('create-order')
        data = {'customer': self.customer.id, 'product': self.product.id, 'quantity': 3}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Order.objects.filter(customer=self.customer, product=self.product, quantity=3).exists())

    def test_average_product_price(self):
        self.client.login(username='customer', password='customerpass')
        url = reverse('average-product-price', args=[self.category.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('average_price', response.data)

    def test_create_category(self):
        self.client.login(username='admin', password='adminpass')
        url = reverse('create-category')
        data = {'name': 'Produce'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Category.objects.filter(name='Produce').exists())
