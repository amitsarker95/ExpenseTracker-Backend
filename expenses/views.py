from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import ExpenseSerializer
from .models import Expense


class ExpenseViewSet(viewsets.ModelViewSet):
    
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

