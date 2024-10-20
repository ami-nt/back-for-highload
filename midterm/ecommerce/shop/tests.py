# tests.py in your app directory
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Order
from django.contrib.auth.models import User

class OrderTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.url = reverse('order-list') 
# Amina Amangeldi
    def test_create_order(self):
        data = {
            'products': [1, 2], 
            'user': self.user.id,
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_orders(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
