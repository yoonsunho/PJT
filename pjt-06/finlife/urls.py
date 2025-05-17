from django.urls import path, include
from . import views

urlpatterns = [

    path('save-deposit-products/', views.save_deposit_products),
    path('deposit-products/', views.deposit_products, name='deposit_products'),
    path('deposit-product-options/<str:fin_prdt_cd>/', views.deposit_product_options, name='deposit_product_options'),
    path('deposit-products/top-rate/', views.deposit_products_top_rate, name='deposit_products_top_rate'),
]