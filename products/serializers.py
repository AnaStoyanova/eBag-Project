from rest_framework import serializers
from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'parent']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'image', 'sku', 'price', 'category']

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError('Price must be greater than zero.')
        return value

    def validate_sku(self, value):
        if not value.replace('-', '').isalnum():
            raise serializers.ValidationError('SKU may only contain letters, numbers, and hyphens.')
        return value.upper()
