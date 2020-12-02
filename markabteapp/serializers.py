from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username',]

class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['order', 'entered_by',]

class OrderCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Order
        fields = ['order', 'entered_by', 'customer',]


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    #write_only so the pw doesn't appear in the response
    password = serializers.CharField(write_only=True)

    #Validate that the username and password combination exist in the database
    def validate(self, data):
        my_username = data.get('username')
        my_password = data.get('password')

        try:
            user_obj = User.objects.get(username=my_username)
        except:
            raise serializers.ValidationError("This username does not exist")

        if not user_obj.check_password(my_password):
            raise serializers.ValidationError("Incorrect username/password combination!")
        
        payload = RefreshToken.for_user(user_obj)
        token = str(payload.access_token)

        data["access"] = token
        return data