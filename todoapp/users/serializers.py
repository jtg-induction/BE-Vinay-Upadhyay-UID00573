
# Add your serializers
from rest_framework import serializers
from .models import CustomUser

class UserBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email']


class UserSerializer(UserBaseSerializer):
    class Meta:
        model = CustomUser
        fields = UserBaseSerializer.Meta.fields + ['id']
