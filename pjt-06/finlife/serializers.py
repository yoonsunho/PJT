from rest_framework import serializers
from .models import DepositProducts, DepositOptions

class DepositProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositProducts
        fields = '__all__'

class DepositOptionsSerializer(serializers.ModelSerializer):
    
    product = serializers.PrimaryKeyRelatedField(queryset=DepositProducts.objects.all())
    
    class Meta:
        model = DepositOptions
        fields = '__all__'