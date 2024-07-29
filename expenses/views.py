from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .serializers import ExpenseSerializer, CategorySerializer, IncomeSerializer
from .models import Expense, Category, Income


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

