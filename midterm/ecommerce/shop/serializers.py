from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Category, Product, Order

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'category']
        

class OrderSerializer(serializers.ModelSerializer):
    products = serializers.PrimaryKeyRelatedField(many=True, queryset=Product.objects.all(), write_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'user', 'products', 'total_price', 'order_date']
        read_only_fields = ['id', 'user', 'total_price', 'order_date']

    def create(self, validated_data):
        products_data = validated_data.pop('products')
        user = self.context['request'].user
        order = Order.objects.create(user=user, **validated_data)
        order.products.set(products_data)
        total_price = sum(product.price for product in products_data)
        order.total_price = total_price
        order.save()
        return order












