from rest_framework import serializers

from .models import User, UserProfile, Buyer, Seller


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data) 
        
        if password is not None:
            instance.set_password(password)
        
        instance.save()

        return instance
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        
        if password is not None:
            instance.set_password(password)
        
        instance.save()

        return instance
    

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['full_name', 'date_of_birth', 'gender', 'address']

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data) 
        instance.save()
        
        return instance