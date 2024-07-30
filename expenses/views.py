from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .serializers import ExpenseSerializer, CategorySerializer, \
    IncomeSerializer, BudgetSerializer , RecurringExpenseSerializer

from .models import Expense, Category, Income, Budget, RecurringExpense


class IncomeViewSet(ModelViewSet):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer


class ExpenseViewSet(ModelViewSet):
    
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    # permission_classes = [IsAuthenticated]

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class BudgetViewSet(ModelViewSet):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer

class RecurringExpenseViewSet(ModelViewSet): 
    queryset = RecurringExpense.objects.all()
    serializer_class = RecurringExpenseSerializer
