from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExpenseViewSet, CategoryViewSet, IncomeViewSet,IncomeDetailViewSet, BudgetViewSet, \
    RecurringExpenseViewSet, SavingsGoalViewSet, TransferToSavingsView

router = DefaultRouter()

router.register('expense', ExpenseViewSet, basename='expenses')
# router.register('category', CategoryViewSet, basename='categories')
# router.register('income', IncomeViewSet, basename='income')
# router.register('budget', BudgetViewSet, basename='budget')
router.register('recurring', RecurringExpenseViewSet, basename='recurring')
# router.register('savings', SavingsGoalViewSet, basename='savings')
urlpatterns = [

    path('', include(router.urls)),
    path('income/', IncomeViewSet.as_view(), name='income'),
    path('income/<int:pk>/', IncomeDetailViewSet.as_view(), name='income-detail'),
    path('budget/', BudgetViewSet.as_view(), name='budget'),
    path('savings/', SavingsGoalViewSet.as_view(), name='savings'),
    path('categories/', CategoryViewSet.as_view(), name='categories'),
    path('transfer-to-savings/', TransferToSavingsView.as_view(), name='transfer-to-savings'),
    
]