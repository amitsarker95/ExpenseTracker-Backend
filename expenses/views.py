from decimal import Decimal
from django.utils.timezone import now
from django.shortcuts import get_object_or_404
from django.db import models
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from django.db.models import Sum
from datetime import timedelta

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

    def create(self, request, *args, **kwargs):
        category = request.data.get('category')
        amount = request.data.get('amount')
        date = request.data.get('date', now().date())

        if not category or not amount:
            return Response({'error': 'category and amount are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            amount = Decimal(amount)
        except ValueError:
            return Response({'error': 'amount must be a number'}, status=status.HTTP_400_BAD_REQUEST)
        
        budget = Budget.objects.filter(
            category__id=category,
            start_date__lte=date,
            end_date__gte=date
        ).first()


        if budget is None:
            return Response({'error': 'Budget for this category not found'}, status=status.HTTP_400_BAD_REQUEST)
        
        total_expense = Expense.objects.filter(
            category__id=category,
            date__range=[budget.start_date, budget.end_date]
        ).aggregate(total=models.Sum('amount'))['total'] or 0
        budget_amount = Decimal(budget.amount)
        remaining_amount = budget_amount - total_expense
        
        if remaining_amount < amount:
            return Response({'error': 'You have exceeded the budget for this category'}, status=status.HTTP_400_BAD_REQUEST)
        
        budget.amount -= amount
        budget.save()

        response = super().create(request, *args, **kwargs)
        return response

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

    def get_queryset(self):
        # Check for expired budgets and update savings
        self.handle_expired_budgets()
        return super().get_queryset()

    def handle_expired_budgets(self):
        today = now().date()
        expired_budgets = Budget.objects.filter(
            end_date__lt=today
        )

        total_savings = Decimal('0')

        for budget in expired_budgets:
            # Calculate total expenses for this budget
            total_expenses = Expense.objects.filter(
                category=budget.category,
                date__range=[budget.start_date, budget.end_date]
            ).aggregate(total=Sum('amount'))['total'] or Decimal('0')

            # Calculate remaining amount
            remaining_amount = budget.amount - total_expenses

            if remaining_amount > 0:
                total_savings += remaining_amount

        if total_savings > 0:
            # Get or create default savings goal
            savings_goal, created = SavingsGoal.objects.get_or_create(
                title="Automatic Budget Savings",
                defaults={
                    'target_amount': Decimal('1000000'),
                    'current_amount': Decimal('0'),
                    'target_date': today + timedelta(days=365),
                    'description': "Accumulated savings from unused budget amounts"
                }
            )

            # Update savings goal
            savings_goal.current_amount += total_savings
            savings_goal.save()

            # Mark processed budgets
            expired_budgets.update(amount=0)

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

class TransferToSavingsView(APIView):
    def post(self, request):
        category_id = request.data.get('category_id')
        date_range_start = request.data.get('start_date')
        date_range_end = request.data.get('end_date')

        try:
            if not all([category_id, date_range_start, date_range_end]):
                return Response(
                    {'error': 'category_id, start_date, and end_date are required'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            budgets = Budget.objects.filter(
                category_id=category_id,
                end_date__range=[date_range_start, date_range_end]
            )

            total_savings = Decimal('0')

            for budget in budgets:
                total_expenses = Expense.objects.filter(
                    category=budget.category,
                    date__range=[budget.start_date, budget.end_date]
                ).aggregate(total=Sum('amount'))['total'] or Decimal('0')

                remaining_amount = budget.amount - total_expenses
                if remaining_amount > 0:
                    total_savings += remaining_amount

            if total_savings > 0:
                savings_goal, created = SavingsGoal.objects.get_or_create(
                    title="Category Savings",
                    defaults={
                        'target_amount': Decimal('1000000'),
                        'current_amount': Decimal('0'),
                        'target_date': now().date() + timedelta(days=365),
                        'description': f"Savings from category {category_id}"
                    }
                )

                savings_goal.current_amount += total_savings
                savings_goal.save()

                budgets.update(amount=0)

                return Response({
                    'message': 'Successfully transferred to savings',
                    'amount': total_savings,
                    'savings_goal_id': savings_goal.id
                }, status=status.HTTP_200_OK)

            return Response({
                'message': 'No remaining amount to transfer'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
