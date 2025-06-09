from rest_framework import serializers
from .models import SecureCipherUser

class SecureCipherUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecureCipherUser
        fields = '__all__'
