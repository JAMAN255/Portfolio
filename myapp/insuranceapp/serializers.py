
from .models import Insurance, Price, InsCategory, InsuranceStatus, CustomerProfile
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = ['id', 'amount', 'currency']

class InsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = InsCategory
        fields = ['id', 'name']

class InsuranceStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceStatus
        fields = ['status']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = ['id', 'name', 'email']
    

class InsuranceSerializer(serializers.ModelSerializer):
    ins_category_id = serializers.PrimaryKeyRelatedField(
        queryset=InsCategory.objects.all(), source='ins_category', write_only=True, required=False, label="Category"
    )
    
    price_id = serializers.PrimaryKeyRelatedField(
        queryset=Price.objects.all(), source='price', write_only=True, required=False, label="Price")
    status_id = serializers.PrimaryKeyRelatedField(
        queryset=InsuranceStatus.objects.all(), source='status', write_only=True, required=False, label="Status")
    ins_category = InsCategorySerializer(read_only=True)
    price = PriceSerializer(read_only=True)
    status = InsuranceStatusSerializer(read_only=True)

    class Meta:
        model = Insurance
        fields = ['id', 'name', 'description', 'ins_category_id', 'ins_category', 'price_id', 'price', 'status_id', 'status']


class UserInsuranceSerializer(serializers.ModelSerializer):
    insurances = InsuranceSerializer(many=True, read_only=True, source='UserInsurance')

    class Meta:
        model = CustomerProfile
        fields = ['id', 'name', 'email', 'is_active', 'insurances']