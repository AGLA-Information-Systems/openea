from rest_framework import serializers

class ObtainTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    organisation = serializers.CharField(required=False)

class RefreshTokenSerializer(serializers.Serializer):
    token = serializers.CharField()
