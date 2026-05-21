
from .models import Insurance, Price, InsCategory, InsuranceStatus, CustomerProfile
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = ['price']

class InsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = InsCategory
        fields = ['ins_category']

class InsuranceStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceStatus
        fields = ['status']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = ['id', 'name', 'email', 'is_active']
    

class InsuranceSerializer(serializers.ModelSerializer):
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=InsCategory.objects.all(), source='category', write_only=True, required=False, label= "Category"
    )
    
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomerProfile.objects.all(), source='user', write_only=True, required=False, label = "User")
    status_id = serializers.PrimaryKeyRelatedField(
        queryset=InsuranceStatus.objects.all(), source = 'status', write_only = True, required = True, label = "Status")
    price_id = serializers.PrimaryKeyRelatedField(
        queryset=Price.objects.all(), source = 'price', write_only = True, required =   True, label = "Price")
    ins_category = InsCategorySerializer(read_only = True)
    user = UserSerializer(read_only = True)
    status = InsuranceStatusSerializer(read_only = True)

    class Meta:
        model = Insurance
        fields = ['id', 'user_id', 'name', 'description', 'price_id', 'price', 'category', 'category_id', 'status', 'status_id']


class UserInsuranceSerializer(serializers.ModelSerializer):
    insurances = InsuranceSerializer(many=True, read_only=True, source='UserInsurance')

    class Meta:
        model = CustomerProfile
        fields = ['id', 'name', 'email', 'is_active', 'insurances']