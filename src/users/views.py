from django.contrib.auth import authenticate
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from . import serializers
from .models import User


class UserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.UserModelSerializer
    queryset = User.objects.all()

    def get_serializer_class(self):
        serializer = super().get_serializer_class()

        if self.action == "create":
            serializer = serializers.SignupRequestSerializer

        return serializer

    @action(methods=["POST"], detail=False)
    def login(self, *args, **kwargs):
        serializer = serializers.LoginRequestSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get("username")
        password = serializer.validated_data.get("password")

        user = authenticate(username=username, password=password)

        if not user:
            return Response(
                {"detail": "Incorrect username or password"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        return Response(serializers.UserModelSerializer(user).data)

    @action(
        methods=["POST"],
        detail=False,
        serializer_class=serializers.SignupRequestSerializer,
    )
    def signup(self, *args, **kwargs):
        return self.create(*args, **kwargs)
