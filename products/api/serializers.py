from rest_framework import serializers
from products.models import Product, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'active')
        depth = 0

class ProductSerializer(serializers.ModelSerializer):
    #category = CategorySerializer()
    class Meta:
        model = Product
        fields = ('id', 'code', 'name', 'desc', 'price', 
                'stock', 'stock_min', 'stock_max', 'active', 'category')
        depth = 0
