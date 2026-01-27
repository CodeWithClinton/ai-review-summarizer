from django.urls import path
from review_app import views

urlpatterns = [
    path('products/<slug:slug>/generate-summary/', views.generate_reviews_summary, name='generate_reviews_summary'),
    path('products/', views.list_products, name='list_products'),
    path('products/<slug:slug>/', views.product_detail, name='product_detail'),
]