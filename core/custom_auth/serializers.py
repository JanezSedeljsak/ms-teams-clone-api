from django.conf import settings
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import EmailConf

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ('username', 'email', 'id', 'first_name', 'last_name', 'password')

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if value == '':
                continue
            
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance

class EmailConfSerailizer(serializers.ModelSerializer):

    class Meta(object):
        model = EmailConf
        fields = ('user', 'uuid')
