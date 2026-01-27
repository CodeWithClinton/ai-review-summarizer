from rest_framework import serializers
from review_app.models import Product, Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'product', 'rating', 'comment', 'author', 'created_at']


class ListProductSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'name', 'image_url', 'price', 'slug', 'reviews']


class ProductDetailSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'image_url', 'description', 'price', 'slug', 'review_summary', 'summary_updated_at', 'reviews']