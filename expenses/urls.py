from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExpenseViewSet, CategoryViewSet, IncomeViewSet, BudgetViewSet, \
    RecurringExpenseViewSet

router = DefaultRouter()

router.register('expense', ExpenseViewSet, basename='expenses')
router.register('category', CategoryViewSet, basename='categories')
router.register('income', IncomeViewSet, basename='income')
router.register('budget', BudgetViewSet, basename='budget')
router.register('recurring', RecurringExpenseViewSet, basename='recurring')

urlpatterns = [
    path('', include(router.urls)),
    
]