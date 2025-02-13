from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
import time
import requests
import logging

class E2ETests(LiveServerTestCase):
    def setUp(self):
        # Set up logging
        logging.basicConfig(level=logging.DEBUG)
        
        # Use the latest version of GeckoDriver for Firefox
        gecko_path = GeckoDriverManager().install()
        logging.debug(f'GeckoDriver path: {gecko_path}')
        
        self.browser = webdriver.Firefox(service=FirefoxService(gecko_path))
        self.admin_user = User.objects.create_user(username='admin22@example.com', password='Zgobjdh89.', email='admin22@example.com', is_superuser=True)
        self.customer_user = User.objects.create_user(username='custome33@example.com', password='Zgobjdh89.', email='customer33@example.com')

    def tearDown(self):
        self.browser.quit()

    def register_user(self, username, password, email):
        response = requests.post(self.live_server_url + '/register/', json={
            'name': username,
            'password': password,
            'email': email
        })
        print(response.json())
        self.assertEqual(response.status_code, 200)

    def get_jwt_token(self, username, password):
        response = requests.post(self.live_server_url + '/login/', json={'username': username, 'password': password})
        self.assertEqual(response.status_code, 200)
        return response.json()['access']

    def login(self, username, password):
        self.browser.get(self.live_server_url + '/login-page/')
        username_input = self.browser.find_element(By.NAME, 'username')
        password_input = self.browser.find_element(By.NAME, 'password')
        username_input.send_keys(username)
        password_input.send_keys(password)
        password_input.send_keys(Keys.RETURN)
        time.sleep(2)  # Wait for the login process to complete

    def test_admin_login(self):
        self.register_user('admin44@example.com', 'Zgobjdh89.', 'admin44@example.com')
        self.login('admin44@example.com', 'Zgobjdh89.')

    def test_customer_login(self):
        self.register_user('customer54@example.com', 'Zgobjdh89.', 'custome54@example.com')
        self.login('customer54@example.com', 'Zgobjdh89.')

    def test_create_category(self):
        self.register_user('admin77@example.com', 'Zgobjdh89.', 'admin77@example.com')
        token = self.get_jwt_token('admin77@example.com', 'Zgobjdh89.')
        headers = {'Authorization': f'Bearer {token}'}
        data = {'name': 'Produce'}
        response = requests.post(self.live_server_url + '/categories/', headers=headers, json=data)
        self.assertEqual(response.status_code, 201)

    def test_create_product(self):
        self.register_user('admin67@example.com', 'Zgobjdh89.', 'admin67@example.com')
        token = self.get_jwt_token('admin67@example.com', 'Zgobjdh89.')
        headers = {'Authorization': f'Bearer {token}'}
        
        # Create a category first
        category_data = {'name': 'Bakery'}
        category_response = requests.post(self.live_server_url + '/categories/', headers=headers, json=category_data)
        self.assertEqual(category_response.status_code, 201)
        category_id = category_response.json()['id']
        
        # Create a product
        product_data = {
            'name': 'Cookies',
            'description': 'Chocolate cookies',
            'price': '2.99',
            'category': category_id
        }
        product_response = requests.post(self.live_server_url + '/products/', headers=headers, json=product_data)
        self.assertEqual(product_response.status_code, 201)

    def test_average_product_price(self):
        self.register_user('customer88@example.com', 'Zgobjdh89.', 'customer88@example.com')
        token = self.get_jwt_token('customer88@example.com', 'Zgobjdh89.')
        headers = {'Authorization': f'Bearer {token}'}
        
        # Create a category and a product first
        category_data = {'name': 'Bakery'}
        category_response = requests.post(self.live_server_url + '/categories/', headers=headers, json=category_data)
        self.assertEqual(category_response.status_code, 201)
        category_id = category_response.json()['id']
        
        product_data = {
            'name': 'Bread',
            'description': 'Fresh bread',
            'price': '1.99',
            'category': category_id
        }
        product_response = requests.post(self.live_server_url + '/products/', headers=headers, json=product_data)
        self.assertEqual(product_response.status_code, 201)
        
        # Get average product price
        avg_price_data = {'category_id': category_id}
        avg_price_response = requests.post(self.live_server_url + '/average-product-price/', headers=headers, json=avg_price_data)
        self.assertEqual(avg_price_response.status_code, 200)
