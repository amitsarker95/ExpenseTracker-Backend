from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExpenseViewSet, CategoryViewSet, IncomeViewSet, BudgetViewSet
router = DefaultRouter()

router.register('expense', ExpenseViewSet, basename='expenses')
router.register('category', CategoryViewSet, basename='categories')
router.register('income', IncomeViewSet, basename='income')
router.register('budget', BudgetViewSet, basename='budget')

urlpatterns = [
    path('', include(router.urls)),
    
]