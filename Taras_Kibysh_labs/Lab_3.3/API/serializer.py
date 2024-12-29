from rest_framework import serializers

from .models import *

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = '__all__'
        # read_only_fields = ['id']

class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = '__all__'

class ItemInsuranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemInsurance
        fields = '__all__'

class CustomerHealthSerializer(serializers.ModelSerializer):
    customer_insuranceinfo = serializers.PrimaryKeyRelatedField(queryset=CustomerInsuranceInfo.objects.all())
    class Meta:
        model = CustomerHealthInsurance
        fields = '__all__'

class WorkerHasCustomerSerializer(serializers.ModelSerializer):
    worker = serializers.PrimaryKeyRelatedField(queryset=Worker.objects.all())
    customer_profile = serializers.PrimaryKeyRelatedField(queryset=CustomerProfile.objects.all())
    class Meta:
        model = WorkerHasCustomerProfile
        fields = ['worker', 'customer_profile']


class InsuranceInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerInsuranceInfo
        fields = '__all__'


class CustomerItemSerializer(serializers.ModelSerializer):
    customer_insuranceinfo = serializers.PrimaryKeyRelatedField(queryset=CustomerInsuranceInfo.objects.all())
    item_insurance = serializers.PrimaryKeyRelatedField(queryset=ItemInsurance.objects.all())
    class Meta:
        model = CustomerItemInsurance
        # fields = ['customer_insuranceinfo', 'item_insurance', 'price_of_item_insurance']
        fields = '__all__'