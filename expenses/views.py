from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import ExpenseSerializer, CategorySerializer, \
    IncomeSerializer, BudgetSerializer , RecurringExpenseSerializer,\
    SavingsGoalSerializer

from .models import Expense, Category, Income, Budget, RecurringExpense, SavingsGoal


class IncomeViewSet(APIView):
    serializer_class = IncomeSerializer

    def get(self, request):
        incomes = Income.objects.all()
        serializer = IncomeSerializer(incomes, many=True)
        return Response(serializer.data)


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

class SavingsGoalViewSet(ModelViewSet):
    queryset = SavingsGoal.objects.all()
    serializer_class = SavingsGoalSerializer
