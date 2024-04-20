from django.urls import path

from .views import (UserRegisterView, UserRetrieveUpdateDestroyView, UserLoginView, CurrentUserRetrieveView, UserLogoutView)

urlpatterns = [
    path('user/register/', UserRegisterView.as_view()),
    path('user/<int:pk>/', UserRetrieveUpdateDestroyView.as_view()),
    path('user/login/', UserLoginView.as_view()),
    path('user/current/', CurrentUserRetrieveView.as_view()),
    path('user/logout/', UserLogoutView.as_view()),
]