from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

from django_filters.rest_framework import DjangoFilterBackend

from .serializers import ExpenseSerializer, CategorySerializer, \
    IncomeSerializer, BudgetSerializer , RecurringExpenseSerializer,\
    SavingsGoalSerializer

from .models import Expense, Category, Income, Budget, RecurringExpense, SavingsGoal
from .pagination import MyPagination
from .filters import BudgetFilterBackend


class IncomeViewSet(APIView):
    serializer_class = IncomeSerializer

    def get(self, request):
        incomes = Income.objects.all()
        serializer = IncomeSerializer(incomes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = IncomeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

class IncomeDetailViewSet(APIView):
    serializer_class = IncomeSerializer
    def get(self, request,pk):
        income = Income.objects.get(pk=pk)
        serializer = IncomeSerializer(income)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk=None):
        income = get_object_or_404(income, pk=pk)
        serializer = IncomeSerializer(income, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


class ExpenseViewSet(ModelViewSet):
    
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    pagination_class = MyPagination

class CategoryViewSet(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        if serializer is not None:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class BudgetViewSet(generics.ListCreateAPIView):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    filter_backends = [DjangoFilterBackend, BudgetFilterBackend]
    filterset_fields = ['amount']

class RecurringExpenseViewSet(ModelViewSet): 
    queryset = RecurringExpense.objects.all()
    serializer_class = RecurringExpenseSerializer

class SavingsGoalViewSet(APIView):
    
    def get(self, request):
        saving_gols = SavingsGoal.objects.all()
        serializer = SavingsGoalSerializer(saving_gols, many=True)
        if serializer is not None:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def post(self, request):
        serializer = SavingsGoalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)