from rest_framework import serializers
from user.models import CustomUser
import re
from django.contrib.auth.hashers import check_password
from rest_framework import permissions

class RegisterUserSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True, required=True)
    password = serializers.CharField(max_length=50, min_length=4, write_only=True)
    password_2 = serializers.CharField(max_length=50, min_length=4, write_only=True)

    def validate(self, data):  # TODO: REGEX
        user = self.context.get('user')

        if user.is_authenticated:
            raise serializers.ValidationError(
                'Извините, вы уже авторизованы'
                )

        if CustomUser.objects.filter(email=data['email']):
            raise serializers.ValidationError(
                'Эта почта занята'
            )

        if not re.findall('\d', data['password']):
            raise serializers.ValidationError(
                ("В пароле обязательно должна быть 1 цифра"),
            )

        if not re.findall('[A-Z]', data['password']):
            raise serializers.ValidationError(
                ("В пароле обязательно нужна одна буква в верхнем регистре"),
            )

        if not re.findall('[a-z]', data['password']):
            raise serializers.ValidationError(
                ("В пароле обязательно нужна одна буква в нижнем регистре"),
            )

        if not re.findall('[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', data['password']):
            raise serializers.ValidationError(
                ("В пароле должен быть 1 символ"),
            )

        if data['password'] != data['password_2']:
            raise serializers.ValidationError(
                ('Пароли не совпадают')
            )

        return data
    
    def create(self, validated_data):
        validated_data.pop('password_2')
        CustomUser.objects.create_user(**validated_data)
        return validated_data


class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        if not CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError('Пользователя с такой почтой не существует')
        return value
    
    def update(self, instance, validated_data):
        return instance

class ConfirmPasswordSerializer(serializers.Serializer):
    
    new_password = serializers.CharField(required=True)

    def validate(self, data):
        if not re.findall('\d', data['new_password']):
            raise serializers.ValidationError(
                ("В пароле обязательно должна быть 1 цифра"),
            )

        if not re.findall('[A-Z]', data['new_password']):
            raise serializers.ValidationError(
                ("В пароле обязательно нужна одна буква в верхнем регистре"),
            )

        if not re.findall('[a-z]', data['new_password']):
            raise serializers.ValidationError(
                ("В пароле обязательно нужна одна буква в нижнем регистре"),
            )

        if not re.findall('[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', data['new_password']):
            raise serializers.ValidationError(
                ("В пароле должен быть 1 символ"),
            )
        
        return data
    
    def update(self, instance, validated_data):
        new_password = validated_data['new_password']
        instance.set_password(new_password)
        instance.save()

        return instance

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        if data['old_password'] == data['new_password']:
            raise serializers.ValidationError(
                'Новый пароль сходится со старым'
            )
        
        if not check_password(data['old_password'], self.instance.password):
            raise serializers.ValidationError(
                'Ваш старый пароль неверный'
            )
        return data
    
    def update(self, instance, validated_data):
        validated_data.pop('old_password')
        new_password = validated_data['new_password']
        instance.set_password(new_password)
        instance.save()

        return instance

class ListUserSerializer(serializers.ModelSerializer):
     
    class Meta:
        model = CustomUser
        fields = "__all__"