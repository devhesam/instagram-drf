from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from rest_framework import serializers

from .models import Follow


class UserRegisterSerailizer(serializers.ModelSerializer):
    
    class Meta:
        model=User
        fields=['fullname','username','phonenumber','password','email']
        extra_kwargs={
            'passwordConfirmation':{'write_only':True},
            'password':{'write_only':True}
        }
        depth=1
       
    def create(self, validated_data):
        password=validated_data.pop('password')
        if password!=self.context['passwordConfirmation']:
            raise ValueError('fc')
        user=User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    username=serializers.StringRelatedField()

    class Meta:
        model=User
        fields=['username']

        
class FollowingSerializer(serializers.ModelSerializer):

    following=UserSerializer()
    class Meta:
        model=Follow
        fields=['following']
        

class FollowerSerializer(serializers.ModelSerializer):

    followers=UserSerializer()
    class Meta:
        model=Follow
        fields=['followers']
        