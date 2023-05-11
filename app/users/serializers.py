from rest_framework import serializers

from app.users.models import User


class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(write_only=True)
    number = serializers.IntegerField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = 'id name number email password confirm_password'.split()

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Данная электронная почта уже используется!')
        return email


    def create(self, validated_data):
        password = validated_data.pop('password')
        confirm_password = validated_data.pop('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError({'password': 'Пароли не совпадают!'})
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

