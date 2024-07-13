from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomUserViewSet, RegisterUserView


router = DefaultRouter()
router.register('users', CustomUserViewSet, basename='users')



urlpatterns = [
    path('', include(router.urls)),
    path('api/register/', RegisterUserView.as_view(), name='register'),
]