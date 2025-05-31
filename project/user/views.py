from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.mail import send_mail
from user.permissions import IsRedactorOrAdmin

from user.models import CustomUser
from user.serializers import RegisterUserSerializer, ForgetPasswordSerializer, ConfirmPasswordSerializer, ChangePasswordSerializer, ListUserSerializer

class RegisterUserAPIView(APIView):

    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data, context={'user':request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response("Вы успешно зарегистрировались!", status=201)

class ForgetPasswordAPIView(APIView):

    def post(self, request):
        email = CustomUser.objects.get(email=request.data['email'])
        serializer = ForgetPasswordSerializer(email, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        send_mail(
            'Здравствуйте',
            f'Чтобы подтвердить сброс пароля перейдите по ссылке http://127.0.0.1:8000/account/confirm/{email.pk}/', 
            'nursaid.seitkozhoev@mail.ru',
            ['pablo0808akd@gmail.com']
        )

        return Response("На почту была отправлена ссылка", status=200)

class ConfirmPasswordAPIView(APIView):
    
    def put(self, request, pk):
        user = CustomUser.objects.get(pk=pk)
        serializer = ConfirmPasswordSerializer(instance=user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response("Вы успешно сменили пароль почты", status=200)

class ChangePasswordAPIView(APIView):

    def put(self, request, pk):
        user = CustomUser.objects.get(pk=pk)
        serializer = ChangePasswordSerializer(instance=user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response("Вы успешно изменили пароль почты", status=200)

class ListUserAPIView(APIView):
    permission_classes = [IsRedactorOrAdmin]
    def get(self, request):
        queryset = CustomUser.objects.all()
        serializer = ListUserSerializer(queryset, many=True)
        return Response(serializer.data, status=200)