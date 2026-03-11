from rest_framework import serializers
from .models import Insurance


class InsuranceSerializer(serializers.Serializer):

    insurance_name = serializers.CharField(required=True, max_length=100)
    policy_number = serializers.CharField(required=True, max_length=100)
    policy_type = serializers.CharField(required=True, max_length=100)
    provider = serializers.CharField(required=True, max_length=100)
    premium = serializers.DecimalField(max_digits=10, decimal_places=2)
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    policy_owner = serializers.SerializerMethodField()

    def get_policy_owner(self, obj):
        return {
            "username": obj.policy_owner.username,
            "email": obj.policy_owner.email,
        }

    def create(self, validate_data):
        return Insurance.objects.create(**validate_data)

    def update(self, instance, validate_data):

        instance.insurance_name = validate_data.get('insurance_name', instance.insurance_name)
        instance.policy_number = validate_data.get('policy_number', instance.policy_number)
        instance.policy_type = validate_data.get('policy_type', instance.policy_type)
        instance.provider = validate_data.get('provider', instance.provider)
        instance.premium = validate_data.get('premium', instance.premium)
        instance.start_date = validate_data.get('start_date', instance.start_date)
        instance.end_date = validate_data.get('end_date', instance.end_date)
        instance.save()
        return instance