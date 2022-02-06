from rest_framework import serializers

from .models import User


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "username", "email")


# request serializeres
class LoginRequestSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class SignupRequestSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = UserModelSerializer.Meta.fields + ("password", "confirm_password")

    def create(self, validated_data):
        instance = super().create(validated_data)

        password = validated_data.get("password")

        instance.set_password(password)
        instance.save()

        return instance

    def validate(self, attrs):
        password = attrs.get("password")
        confirm_password = attrs.pop("confirm_password")

        if password != confirm_password:
            raise serializers.ValidationError(
                "confirm password and password must be the same"
            )

        return attrs
