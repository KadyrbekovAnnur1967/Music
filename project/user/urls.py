from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from user.views import RegisterUserAPIView, ForgetPasswordAPIView, ConfirmPasswordAPIView, ChangePasswordAPIView, ListUserAPIView

urlpatterns = [
  
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterUserAPIView.as_view()),
    path('forget/', ForgetPasswordAPIView.as_view()),
    path('confirm/<int:pk>/', ConfirmPasswordAPIView.as_view()),
    path('change/<int:pk>/', ChangePasswordAPIView.as_view()),
    path('list_user/', ListUserAPIView.as_view()),
]