from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExpenseViewSet
router = DefaultRouter()

router.register('expense', ExpenseViewSet, basename='expenses')

urlpatterns = [
    path('', include(router.urls)),
]