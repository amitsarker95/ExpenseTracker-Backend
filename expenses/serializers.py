from rest_framework import serializers
from .models import Expense, Income, Budget

class ExpenseSerializer(serializers.ModelSerializer):
    
    user_name = serializers.ReadOnlyField(source="user_full_name")

    class Meta:
        model = Expense
        fields = ['id','user_name','title','description','amount','category','date']


class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ['id','title', 'amount', 'date','description']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = instance.user.first_name
        return representation
    

class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields =['id','category','amount','start_date','end_date']

