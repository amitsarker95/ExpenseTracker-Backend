from rest_framework import serializers
from .models import Expense

class ExpenseSerializer(serializers.ModelSerializer):
    
    user_name = serializers.ReadOnlyField(source="user_full_name")

    class Meta:
        model = Expense
        fields = ['id','user_name','title','description','amount','category','date']

