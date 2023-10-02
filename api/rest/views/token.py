from django.contrib.auth import get_user_model
from rest_framework import views, permissions, status
from rest_framework.response import Response

from api.rest.serializers import ObtainTokenSerializer
from api.controllers.jwt import JWTController
from api.rest.serializers.token import RefreshTokenSerializer

User = get_user_model()

class ObtainTokenView(views.APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ObtainTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        username_or_phone_number = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')

        user = User.objects.filter(username=username_or_phone_number).first()
        if user is None:
            user = User.objects.filter(phone_number=username_or_phone_number).first()

        if user is None or not user.check_password(password):
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        # Generate the JWT token
        jwt_token = JWTController.create_jwt(user)

        return Response({'token': jwt_token})


class RefreshTokenView(views.APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RefreshTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data.get('token')

        username = token.get('user')
        if username is not None:
            user = User.objects.filter(phone_number=username).first()

        if user is None:
            return Response({'message': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

        # Generate the JWT token
        jwt_token = JWTController.create_jwt(user)

        return Response({'token': jwt_token})