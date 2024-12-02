from rest_framework import serializers
from .models import Product, Stock, StockProduct
from django_filters import rest_framework as filters


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']

class ProductPositionSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']

class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['address', 'positions']

    def create(self, validated_data):
        positions_data = validated_data.pop('positions')
        stock = Stock.objects.create(**validated_data)
        for position_data in positions_data:
            StockProduct.objects.create(stock=stock, **position_data)
        return stock

    def update(self, instance, validated_data):
        positions_data = validated_data.pop('positions')
        instance.address = validated_data.get('address', instance.address)
        instance.save()
        for position_data in positions_data:
            StockProduct.objects.update_or_create(stock=instance, product=position_data['product'], defaults={'quantity': position_data['quantity'], 'price': position_data['price']})
        return instance

class StockFilter(filters.FilterSet):
    products = filters.NumberFilter(field_name='positions__product__id', distinct=True)

    class Meta:
        model = Stock
        fields = ['address', 'positions__product__id']