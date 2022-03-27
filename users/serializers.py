from xml.etree.ElementInclude import include
from rest_framework import serializers
from .models import NewUser as Users


class CustomUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    user_name = serializers.CharField(required=True)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = Users
        fields = ('email', 'user_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    # def validate_email(self, email):
    #     existing = Users.objects.filter(email=email).first()
    #     if existing:
    #         raise serializers.ValidationError({"error": "email_error",
    #                                            "messege": "This email address is already used by another account."},)
    #     return email

    # def validate_user_name(self, user_name):
    #     existing = Users.objects.filter(user_name=user_name).first()
    #     if existing:
    #         raise serializers.ValidationError({"error": "user_name_error",
    #                                            "messege": "User name already exists, please choose another one."})
    #     if len(user_name) < 3:
    #         raise serializers.ValidationError({"error": "user_name_error",
    #                                            "messege": "User name must be at least 3 characters long."})
    #     return user_name

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        exclude = ('password', 'is_active', 'is_staff',
                   'is_superuser', 'date_joined')
