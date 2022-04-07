from rest_framework import serializers
from .models import NewUser as Users
from api.models import Noodle


class NoodleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Noodle
        fields = ('id', "name", 'slug')


class CustomUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    user_name = serializers.CharField(required=True)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = Users
        fields = ('email', 'user_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class UserDetailsSerializer(serializers.ModelSerializer):
    favorites = NoodleSerializer(many=True, read_only=True)

    class Meta:
        model = Users
        fields = ('id', 'email', 'user_name', 'favorites')
        # exclude = ('password', 'is_active', 'is_staff',
        #            'is_superuser', )
